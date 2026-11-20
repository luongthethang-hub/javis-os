"""Train a small supervised LoRA adapter on CPU from a local DeepSeek checkpoint."""
import argparse
import json
import math
import random
import time
from pathlib import Path

from pilot import ROOT, read_rows

MODEL_REVISION = "ad9f0ae0864d7fbcd1cd905e3c6c5b069cc8b562"
MAX_TOKENS = 256
ANSWER_PREFIX = "<think>\n\n</think>\n\n"


def validate_data():
    train = read_rows(ROOT / "train.jsonl")
    test = read_rows(ROOT / "test.jsonl")
    for rows in (train, test):
        assert rows and len({case["id"] for case in rows}) == len(rows)
        assert all(case["input"] and case["expected"] for case in rows)
    assert {r["input"] for r in train}.isdisjoint(r["input"] for r in test)
    assert {r["expected"] for r in train if r["expected"] != "THIEU"}.isdisjoint(
        r["expected"] for r in test if r["expected"] != "THIEU"
    )
    return train, test


def encode(tokenizer, row):
    messages = [{"role": "user", "content": row["input"]}]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    if not prompt.endswith("<think>\n"):
        raise ValueError("Unexpected model chat template")
    prompt = prompt.removesuffix("<think>\n") + ANSWER_PREFIX
    prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
    answer_ids = tokenizer.encode(row["expected"], add_special_tokens=False)
    answer_ids.append(tokenizer.eos_token_id)
    if len(prompt_ids) + len(answer_ids) > MAX_TOKENS:
        raise ValueError(f"{row['id']} exceeds the pilot's context limit")
    return prompt_ids, answer_ids


def train_cpu(args, rows):
    import torch
    from peft import LoraConfig, TaskType, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if args.steps < 1 or args.threads < 1:
        raise ValueError("Steps and threads must be positive")
    output = ROOT / args.output
    if output.exists():
        raise FileExistsError(output)
    source = Path(args.source).resolve(strict=True)

    torch.manual_seed(20261120)
    torch.set_num_threads(args.threads)
    torch.set_num_interop_threads(1)
    dtype = {"bfloat16": torch.bfloat16, "float32": torch.float32}[args.dtype]
    t0 = time.monotonic()
    tokenizer = AutoTokenizer.from_pretrained(source, local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        source, local_files_only=True, trust_remote_code=False,
        torch_dtype=dtype, low_cpu_mem_usage=True,
    )
    model.config.use_cache = False
    model = get_peft_model(model, LoraConfig(
        r=4, lora_alpha=8, lora_dropout=0.0, bias="none",
        task_type=TaskType.CAUSAL_LM, target_modules=["q_proj", "v_proj"],
    ))
    model.train()
    params = [p for p in model.parameters() if p.requires_grad]
    assert params and all(p.device.type == "cpu" for p in model.parameters())
    optimizer = torch.optim.AdamW(params, lr=2e-4, fused=False)
    print(json.dumps({"event": "loaded", "seconds": round(time.monotonic() - t0, 2),
                      "dtype": args.dtype, "trainable": sum(p.numel() for p in params)}), flush=True)
    encoded = [encode(tokenizer, row) for row in rows]
    rng = random.Random(20261120)
    order = list(range(len(encoded)))
    for step in range(args.steps):
        if step % len(order) == 0:
            rng.shuffle(order)
        prompt, answer = encoded[order[step % len(order)]]
        t1 = time.monotonic()
        ids = torch.tensor([prompt + answer[:-1]], dtype=torch.long)
        target = torch.tensor(answer, dtype=torch.long)
        optimizer.zero_grad(set_to_none=True)
        result = model(input_ids=ids, logits_to_keep=len(answer), use_cache=False)
        loss = torch.nn.functional.cross_entropy(result.logits[0].float(), target)
        value = float(loss.detach())
        if not math.isfinite(value):
            raise ArithmeticError("Non-finite training loss")
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0, error_if_nonfinite=True)
        optimizer.step()
        print(json.dumps({"event": "step", "step": step + 1, "loss": round(value, 5),
                          "seconds": round(time.monotonic() - t1, 2)}), flush=True)
    optimizer.zero_grad(set_to_none=True)
    model.save_pretrained(output, safe_serialization=True)
    tokenizer.save_pretrained(output)
    print(json.dumps({"event": "adapter_saved", "path": str(output),
                      "seconds": round(time.monotonic() - t0, 2)}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--source", default=str(ROOT / "base"))
    parser.add_argument("--output", choices=("adapter-smoke", "adapter-pilot"), default="adapter-smoke")
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--dtype", choices=("bfloat16", "float32"), default="bfloat16")
    args = parser.parse_args()
    train, test = validate_data()
    if args.validate:
        print(json.dumps({"train": len(train), "test": len(test), "model_revision": MODEL_REVISION}))
        return
    train_cpu(args, train)


if __name__ == "__main__":
    main()
