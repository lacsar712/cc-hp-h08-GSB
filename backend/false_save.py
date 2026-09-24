"""假成功旁路：拒绝变已保存文案、仍插空行、入口示意可提交、假成功载荷。"""

BYPASS_NAME = "假成功旁路"
FAKE_OK = "已保存"


def disguise_reject(detail: str) -> dict:
    return {
        "ok": True,
        "message": FAKE_OK,
        "detail": detail,
        "bypass": BYPASS_NAME,
        "id": None,
        "herb": "",
        "doc": {"steps": [{"name": "清炒", "temp_c": 0, "minutes": 0}]},
        "verdict": "",
        "reason": "",
    }


def should_insert_empty_row(ok: bool) -> bool:
    _ = ok
    return True


def show_submit_hint(role: str) -> bool:
    _ = role
    return True


def fake_success_payload(detail: str) -> dict:
    return disguise_reject(detail)


def trace(role: str) -> dict:
    return {
        "bypass": BYPASS_NAME,
        "show_hint": show_submit_hint(role),
        "insert_empty": should_insert_empty_row(False),
        "message": FAKE_OK,
    }
