from bitbanker_sdk.utils import generate_sign


def test_generate_sign() -> None:
    sign = generate_sign('message', 'key')
    assert sign == '6e9ef29b75fffc5b7abae527d58fdadb2fe42e7219011976917343065f58ed4a'
