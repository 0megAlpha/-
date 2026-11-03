# Cloud-vps unified repo
每個 agent 一個資料夾，可單獨拉取：

    git clone --filter=blob:none --sparse <repo-url> && cd Cloud-vps
    git sparse-checkout set agents/hermes

- agents/<name>/   各 agent 的自有檔案、docker 摘要、systemd unit
- gateway/         litellm / 9router / new-api / nginx / caddy
- local-llm/       本機模型服務設定（不含模型檔）
- skills/          技能包
- ops/             套件清單、crontab、監聽 port 快照
- upstreams.tsv    第三方上游 repo（URL + pinned commit）
- patches/<name>/  對上游的本地修改（format-patch / dirty.diff）
- scripts/sync-upstream.sh  拉最新上游並套用 patches
