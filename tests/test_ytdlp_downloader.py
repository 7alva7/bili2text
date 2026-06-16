from b2t.config import Settings
from b2t.downloaders.ytdlp import YtDlpDownloader
from b2t.models import SourceRef


def test_ytdlp_options_keep_single_video_output_template_by_default(tmp_path) -> None:
    settings = Settings.from_workspace(tmp_path / ".b2t")
    source = SourceRef(
        raw_input="BV1xx411c7XD",
        kind="bilibili",
        display_name="BV1xx411c7XD",
        bv="BV1xx411c7XD",
        url="https://www.bilibili.com/video/BV1xx411c7XD",
    )

    opts = YtDlpDownloader()._build_ydl_opts(source, settings)

    assert opts["noplaylist"] is True
    assert "playlist_items" not in opts
    assert opts["outtmpl"] == str(settings.downloads_dir / "%(id)s.%(ext)s")


def test_ytdlp_options_select_playlist_item_when_page_is_set(tmp_path) -> None:
    settings = Settings.from_workspace(tmp_path / ".b2t")
    source = SourceRef(
        raw_input="https://www.bilibili.com/video/BV1xx411c7XD?p=2",
        kind="bilibili",
        display_name="BV1xx411c7XD",
        bv="BV1xx411c7XD",
        url="https://www.bilibili.com/video/BV1xx411c7XD?p=2",
        page=2,
    )

    opts = YtDlpDownloader()._build_ydl_opts(source, settings)

    assert opts["noplaylist"] is False
    assert opts["playlist_items"] == "2"
    assert opts["outtmpl"] == str(settings.downloads_dir / "%(id)s.%(playlist_index)02d.%(ext)s")


def test_ytdlp_options_bypass_proxy_by_default(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("B2T_USE_PROXY", raising=False)
    settings = Settings.from_workspace(tmp_path / ".b2t")
    source = SourceRef(
        raw_input="BV1xx411c7XD",
        kind="bilibili",
        display_name="BV1xx411c7XD",
        bv="BV1xx411c7XD",
        url="https://www.bilibili.com/video/BV1xx411c7XD",
    )

    opts = YtDlpDownloader()._build_ydl_opts(source, settings)

    assert opts["proxy"] == ""


def test_ytdlp_options_keep_system_proxy_when_enabled(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("B2T_USE_PROXY", "1")
    settings = Settings.from_workspace(tmp_path / ".b2t")
    source = SourceRef(
        raw_input="BV1xx411c7XD",
        kind="bilibili",
        display_name="BV1xx411c7XD",
        bv="BV1xx411c7XD",
        url="https://www.bilibili.com/video/BV1xx411c7XD",
    )

    opts = YtDlpDownloader()._build_ydl_opts(source, settings)

    assert "proxy" not in opts


def test_ytdlp_options_falsey_proxy_flag_still_bypasses(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("B2T_USE_PROXY", "0")
    settings = Settings.from_workspace(tmp_path / ".b2t")
    source = SourceRef(
        raw_input="BV1xx411c7XD",
        kind="bilibili",
        display_name="BV1xx411c7XD",
        bv="BV1xx411c7XD",
        url="https://www.bilibili.com/video/BV1xx411c7XD",
    )

    opts = YtDlpDownloader()._build_ydl_opts(source, settings)

    assert opts["proxy"] == ""
