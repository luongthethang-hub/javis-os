"""Merge a locally trained adapter and reuse the original Ollama prompt template."""
import argparse
import json
import re
import subprocess
import time

from pilot import ROOT


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", choices=("adapter-smoke", "adapter-pilot"), default="adapter-pilot")
    args = parser.parse_args()

    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    base_path = ROOT / "base"
    adapter_path = ROOT / args.adapter
    if not (adapter_path / "adapter_model.safetensors").is_file():
        raise FileNotFoundError(adapter_path / "adapter_model.safetensors")
    output = ROOT / args.adapter.replace("adapter-", "merged-")
    if output.exists():
        raise FileExistsError(output)

    torch.set_num_threads(4)
    t0 = time.monotonic()
    base = AutoModelForCausalLM.from_pretrained(
        base_path, local_files_only=True, trust_remote_code=False,
        dtype=torch.bfloat16, low_cpu_mem_usage=True,
    )
    model = PeftModel.from_pretrained(base, adapter_path, is_trainable=False)
    merged = model.merge_and_unload(safe_merge=True)
    merged.config.use_cache = True
    token = AutoTokenizer.from_pretrained(base_path, local_files_only=True, trust_remote_code=False)
    merged.save_pretrained(output, safe_serialization=True, max_shard_size="512MB")
    token.save_pretrained(output)

    original = subprocess.check_output(
        ["ollama", "show", "--modelfile", "deepseek-r1:1.5b"], encoding="utf-8",
    )
    modelfile, count = re.subn(r"(?m)^FROM [^\r\n]+$", "FROM ./" + output.name, original)
    if count != 1:
        raise ValueError("Unexpected Ollama model definition")
    (ROOT / ("Modelfile-" + args.adapter)).write_text(modelfile, encoding="utf-8")
    print(json.dumps({"event": "merged", "path": str(output),
                      "seconds": round(time.monotonic() - t0, 2)}), flush=True)


if __name__ == "__main__":
    main()
