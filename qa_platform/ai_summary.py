"""失败结果摘要：默认本地规则；有 API Key 时可调用大模型。"""

from __future__ import annotations

import os
import re
from pathlib import Path


PROMPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "ai-qa-kit"
    / "prompts"
    / "failure_summarize.md"
)


def ai_summary_enabled() -> bool:
    return os.environ.get("QA_AI_SUMMARY", "1").strip() not in {"0", "false", "False"}


def summarize_failure(
    *,
    job_id: int,
    passed: int,
    failed: int,
    total: int,
    message: str,
) -> str:
    """生成失败摘要。摘要失败不影响主流程，返回空字符串。"""
    if not ai_summary_enabled() or failed <= 0:
        return ""

    try:
        rule_text = _rule_based_summary(job_id, passed, failed, total, message)
        llm_text = _optional_llm_summary(job_id, passed, failed, total, message)
        if llm_text:
            return llm_text
        return rule_text
    except Exception as exc:  # noqa: BLE001 - 摘要绝不能拖垮交卷
        return f"[摘要跳过] 生成失败：{exc}"


def _rule_based_summary(
    job_id: int,
    passed: int,
    failed: int,
    total: int,
    message: str,
) -> str:
    failed_lines = [
        line.strip()
        for line in (message or "").splitlines()
        if "FAILED" in line or "AssertionError" in line or "E       " in line
    ]
    highlight = failed_lines[:5]
    assert_match = re.search(r"assert\s+.+=.+", message or "")
    facts = [
        f"任务 #{job_id} 执行结果：passed={passed}, failed={failed}, total={total}",
        "事实：存在失败用例，需要排查断言或环境问题。",
    ]
    if assert_match:
        facts.append(f"事实：日志中出现 `{assert_match.group(0)[:120]}`")
    if highlight:
        facts.append("日志摘要：")
        facts.extend(f"- {line[:160]}" for line in highlight)
    else:
        facts.append("日志摘要：未解析到 FAILED 行，请查看完整 message。")

    facts.append("[推测] 可能是断言期望与实际不符，或依赖服务不稳定（需人工确认）。")
    facts.append("TODO：对照用例步骤复现，并区分产品缺陷 / 用例问题 / 环境问题。")
    return "\n".join(facts)


def _optional_llm_summary(
    job_id: int,
    passed: int,
    failed: int,
    total: int,
    message: str,
) -> str:
    """若配置了 QA_AI_API_KEY（或 OPENAI_API_KEY），尝试调用兼容接口。"""
    api_key = os.environ.get("QA_AI_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return ""

    base_url = os.environ.get("QA_AI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("QA_AI_MODEL", "gpt-4o-mini")
    prompt = _load_prompt().format(
        JOB_ID=job_id,
        PASSED=passed,
        FAILED=failed,
        TOTAL=total,
        LOG=(message or "")[:3000],
    )

    try:
        import requests

        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "temperature": 0.2,
                "messages": [
                    {
                        "role": "system",
                        "content": "你是资深测试工程师。只根据日志总结，不要编造。",
                    },
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=20,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return str(content).strip()
    except Exception:  # noqa: BLE001
        return ""


def _load_prompt() -> str:
    if PROMPT_PATH.exists():
        return PROMPT_PATH.read_text(encoding="utf-8")
    return (
        "任务 #{JOB_ID}，passed={PASSED}, failed={FAILED}, total={TOTAL}\n"
        "日志：\n{LOG}\n"
        "请输出：事实摘要、可能原因（标推测）、建议下一步。"
    )
