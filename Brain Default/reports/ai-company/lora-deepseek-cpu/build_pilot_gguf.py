"""Rebuild the trained Q/V matrices with the same quantized types as stock Ollama."""
import ctypes as ct
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

import gguf
import numpy as np
from safetensors import safe_open
import torch

from pilot import ROOT

STOCK_MODEL = "deepseek-r1:1.5b"


def bind_quantizer(dll):
    library = ct.CDLL(str(dll))
    library.ggml_quantize_requires_imatrix.argtypes = [ct.c_int]
    library.ggml_quantize_requires_imatrix.restype = ct.c_bool
    library.ggml_row_size.argtypes = [ct.c_int, ct.c_int64]
    library.ggml_row_size.restype = ct.c_size_t
    library.ggml_quantize_chunk.argtypes = [
        ct.c_int, ct.c_void_p, ct.c_void_p,
        ct.c_int64, ct.c_int64, ct.c_int64, ct.c_void_p,
    ]
    library.ggml_quantize_chunk.restype = ct.c_size_t
    return library


def quantize(matrix, tensor, ggml):
    rows, cols = matrix.shape
    kind = tensor.tensor_type
    if tuple(tensor.shape) != (cols, rows):
        raise ValueError(f"Unexpected matrix shape for {tensor.name}")
    if ggml.ggml_quantize_requires_imatrix(kind):
        raise ValueError(f"{kind.name} needs an importance matrix")
    size = rows * ggml.ggml_row_size(kind, cols)
    if size != tensor.n_bytes:
        raise ValueError(f"Unexpected serialized size for {tensor.name}")
    target = ct.create_string_buffer(size)
    written = ggml.ggml_quantize_chunk(kind, matrix.ctypes.data, target, 0, rows, cols, None)
    if written != size:
        raise ValueError(f"Quantized byte count differs for {tensor.name}")
    return target.raw


def write_model(name, original, modelfile, regions):
    output = ROOT / f"{name}.gguf"
    part = output.with_suffix(".gguf.part")
    if output.exists() or part.exists():
        raise FileExistsError(output)
    with original.open("rb") as source, part.open("xb") as copied:
        shutil.copyfileobj(source, copied, length=8 * 2**20)
    with part.open("r+b") as model:
        for offset, data in regions:
            model.seek(offset)
            model.write(data)
    reader = gguf.GGUFReader(part)
    if output.exists() or reader.get_field("general.architecture").contents() != "qwen2":
        raise ValueError("Output validation failed")
    del reader
    part.rename(output)
    definition, count = re.subn(r"(?m)^FROM [^\r\n]+$", "FROM ./" + output.name, modelfile)
    if count != 1:
        raise ValueError("Unexpected original model definition")
    (ROOT / ("Modelfile-" + name)).write_text(definition, encoding="utf-8")


def main():
    torch.set_num_threads(2)
    ollama = Path(shutil.which("ollama")).resolve()
    definitions = subprocess.check_output(
        [str(ollama), "show", "--modelfile", STOCK_MODEL], encoding="utf-8",
    )
    from_lines = [line[5:].strip().strip('"') for line in definitions.splitlines() if line.startswith("FROM ")]
    if len(from_lines) != 1:
        raise ValueError("Unexpected stock model definition")
    original = Path(from_lines[0]).resolve(strict=True)
    expected = original.name.removeprefix("sha256-")
    with original.open("rb") as file:
        if hashlib.file_digest(file, "sha256").hexdigest() != expected:
            raise ValueError("Unexpected original GGUF hash")
    base_reader = gguf.GGUFReader(original)
    if base_reader.get_field("general.architecture").contents() != "qwen2":
        raise ValueError("Unexpected stock architecture")
    all_tensors = {item.name: item for item in base_reader.tensors}
    adapter = json.loads((ROOT / "adapter-pilot" / "adapter_config.json").read_text())
    merged = ROOT / "merged-pilot"
    index = json.loads((merged / "model.safetensors.index.json").read_text())["weight_map"]
    variants = {"pilot": [], "control": []}
    metrics = []
    dll_dir = ollama.parent / "lib" / "ollama"
    with os.add_dll_directory(dll_dir), safe_open(
        ROOT / "base" / "model.safetensors", framework="pt", device="cpu",
    ) as base:
        ggml = bind_quantizer(dll_dir / "ggml-base.dll")
        for layer in adapter["layers_to_transform"]:
            for source, dest in (("q_proj", "attn_q"), ("v_proj", "attn_v")):
                hf_name = f"model.layers.{layer}.self_attn.{source}.weight"
                tensor = all_tensors[f"blk.{layer}.{dest}.weight"]
                base_matrix = base.get_tensor(hf_name).float().contiguous().numpy()
                decoded = gguf.dequantize(tensor.data, tensor.tensor_type)
                similarity = float(np.corrcoef(base_matrix.reshape(-1), decoded.reshape(-1))[0, 1])
                if not np.isfinite(similarity) or similarity < 0.98:
                    raise ValueError(f"Stock matrix does not match checkpoint: {tensor.name}, {similarity}")
                with safe_open(merged / index[hf_name], framework="pt", device="cpu") as shard:
                    tuned_matrix = shard.get_tensor(hf_name).float().contiguous().numpy()
                control = quantize(base_matrix, tensor, ggml)
                tuned = quantize(tuned_matrix, tensor, ggml)
                variants["control"].append((int(tensor.data_offset), control))
                variants["pilot"].append((int(tensor.data_offset), tuned))
                row = {
                    "name": tensor.name, "quant": tensor.tensor_type.name,
                    "stock_correlation": round(similarity, 5),
                    "control_equals_stock": control == tensor.data.tobytes(),
                    "tuned_differs_from_control": tuned != control,
                }
                metrics.append(row)
                print(json.dumps(row), flush=True)
    if len(metrics) != 8 or not all(m["tuned_differs_from_control"] for m in metrics):
        raise ValueError("LoRA effects were not preserved in the eight tuned weight matrices")
    write_model("pilot-gguf", original, definitions, variants["pilot"])
    if not all(m["control_equals_stock"] for m in metrics):
        write_model("control-gguf", original, definitions, variants["control"])
    (ROOT / "conversion.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
