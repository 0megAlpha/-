# 四大 Agent 平台可掛載生態全攻略（2026-09 選品）

> 涵蓋：Hermes Agent（70 項）、DeepSeek Harness / DSH（70 項）、OpenWebUI（70 項）、OpenHands（60 項）
> 依你的要求：**一律不標示 port 號與版本號**；Docker 指令如需對外連線請自行依環境補上 `-p` 映射。
> 所有條目皆為「可安裝、可掛載、可使用」導向：官方安裝指令、經查證的上游/社群套件、或以 heredoc 一鍵寫入的 skill 檔（貼上即生效）。

---

# 一、Hermes Agent（Nous Research）— 70 項

Hermes Agent 是 Nous Research 2026-02-25 開源的自進化 agent 框架（MIT），核心特性：自動生成/改進 SKILL.md 技能、USER.md 使用者建模、40+ 內建工具、MCP 擴充、自然語言 cron、多沙箱後端（Docker/Modal/Daytona/SSH/Singularity/本機）、13 種通訊平台。

## 1-1. 核心安裝（官方 4 式 + 周邊 2 式）

**01｜官方一鍵安裝（Linux/macOS/WSL2）**
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc
hermes
```

**02｜開發者 bootstrap（推薦：可改可除錯）**
```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
./setup-hermes.sh
./hermes
```

**03｜手動 uv 安裝**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install -e ".[all,dev]"
scripts/run_tests.sh
```

**04｜Hermes WebUI（手機/瀏覽器操作介面，非官方）**
```bash
git clone https://github.com/nesquena/hermes-webui.git
cd hermes-webui
./install.sh
```

**05｜非官方 Helm Chart（K8s 部署）**
```bash
git clone https://github.com/ultraworkers/hermes-agent-helm-chart.git
cd hermes-agent-helm-chart
helm install hermes .
```

**06｜自我進化外掛（DSPy + GEPA）**
```bash
git clone https://github.com/NousResearch/hermes-agent-self-evolution.git
cd hermes-agent-self-evolution
pip install -e .
```

## 1-2. 工具集 / 整合（20 項，寫入 `~/.hermes/config.yaml` 或 pip 安裝）

**07｜GitHub 工具集** — config.yaml 加入：
```yaml
toolsets:
- github
- terminal
```

**08｜Docker 沙箱後端**
```yaml
terminal:
  backend: docker
  container_persistent: true
```

**09｜Modal 雲端沙箱** `pip install modal && modal setup`
**10｜Daytona 沙箱** `curl -fsSL https://get.daytona.io | bash`
**11｜SSH 遠端沙箱** — config.yaml `terminal: {backend: ssh, ssh_host: ...}`
**12｜Singularity（HPC）** — config.yaml `terminal: {backend: singularity}`
**13｜MCP filesystem server** — config.yaml `mcp_servers: [{name: fs, command: npx, args: ["-y","@modelcontextprotocol/server-filesystem","/path"]}]`
**14｜MCP GitHub server** `npm i -g @modelcontextprotocol/server-github`
**15｜MCP Postgres server** `pip install mcp-server-postgres`
**16｜MCP fetch / memory / sequential-thinking** `npm i -g @modelcontextprotocol/server-fetch @modelcontextprotocol/server-memory @modelcontextprotocol/server-sequential-thinking`
**17｜MCP Playwright（瀏覽器自動化）** `npm i -g @playwright/mcp && npx playwright install chromium`
**18｜瀏覽器工具 browser-use** `pip install browser-use`
**19｜Firecrawl 爬蟲** `pip install firecrawl-py`
**20｜Browserbase 雲端瀏覽器** `npm i -g @browserbasehq/mcp-server-browserbase`
**21｜Telegram 頻道** — config.yaml `gateway: {platforms: [telegram]}` + bot token
**22｜Discord/Slack/WhatsApp/Signal/Email 頻道** — 同上，平台清單選配
**23｜語音 TTS（ElevenLabs/OpenAI）** `pip install elevenlabs openai`
**24｜ACP IDE 整合（VS Code / Zed / JetBrains）** `pip install acp-sdk`
**25｜Obsidian 第二腦（記憶庫）** — 建立 `~/obsidian-vault`，config 指向，HERMES 以 USER.md + episodic SQLite 存取
**26｜自然語言排程範例** `hermes -c "每天早八點生成本日研究簡報"`

## 1-3. Skills 44 顆（一鍵寫入 `~/.hermes/skills/`，11 個區塊，貼上即完成）

**27-30｜Android 除錯 / Termux / Flutter / React Native**
```bash
mkdir -p ~/.hermes/skills/{android-debug,termux-bootstrap,flutter-ci,react-native-expo}
cat > ~/.hermes/skills/android-debug/SKILL.md <<'EOF'
---
name: android-debug
description: ADB logcat 結構化分析：崩潰堆疊定位、ANR 解析、效能瓶頸
---
## Procedure
1. `adb devices` 確認連線；`adb logcat -b crash` 取崩潰堆疊
2. 以 FATAL EXCEPTION 行為錨點，往回 50 行收集上下文
3. ANR：取 /data/anr/traces.txt，分析主執行緒阻塞點
4. 輸出：崩潰類型、可疑檔案:行號、復現步驟、修復建議
EOF
cat > ~/.hermes/skills/termux-bootstrap/SKILL.md <<'EOF'
---
name: termux-bootstrap
description: Termux 手機開發環境一鍵初始化（proot-distro、clang、python、git）
---
## Procedure
1. `pkg update && pkg upgrade -y`
2. `pkg install -y git clang python nodejs-lts proot-distro`
3. `proot-distro install debian && proot-distro login debian`
4. 驗證：gcc/python/node 各跑 --version
EOF
cat > ~/.hermes/skills/flutter-ci/SKILL.md <<'EOF'
---
name: flutter-ci
description: Flutter 專案 CI 建置腳本與常見錯誤排查
---
## Procedure
1. `flutter analyze` 零錯誤為前提
2. `flutter test --coverage`，回報覆蓋率
3. `flutter build apk --split-per-abi` 產物檢查
4. 常見坑：Gradle daemon 卡死→`./gradlew --stop`；版本衝突→`flutter pub deps --style=tree`
EOF
cat > ~/.hermes/skills/react-native-expo/SKILL.md <<'EOF'
---
name: react-native-expo
description: Expo/React Native 開發流程：EAS Build、OTA 更新、除錯
---
## Procedure
1. `npx expo start` 開發；搖手機開 Dev Menu
2. EAS：`npm i -g eas-cli && eas build --platform android`
3. OTA：`eas update --branch production`
4. 原生模組需求→`npx expo prebuild`
EOF
```

**31-34｜Kotlin Compose / SwiftUI / Capacitor / fastlane**
```bash
mkdir -p ~/.hermes/skills/{kotlin-compose-review,swiftui-review,capacitor-build,fastlane-release}
cat > ~/.hermes/skills/kotlin-compose-review/SKILL.md <<'EOF'
---
name: kotlin-compose-review
description: Jetpack Compose 程式碼審查：recomposition 效能、狀態 hoisting、副作用正確性
---
## Procedure
1. 檢查 Composable 是否讀取非 snapshot 狀態
2. 找出缺 remember/rememberSaveable 的昂貴計算
3. LazyColumn key 正確性、derivedStateOf 使用時機
4. 回報：效能風險分級（block/major/minor）+ 修改 patch
EOF
cat > ~/.hermes/skills/swiftui-review/SKILL.md <<'EOF'
---
name: swiftui-review
description: SwiftUI 審查：View 拆解、@State/@Binding 層級、ObservableObject 生命週期
---
## Procedure
1. 主 View 超過 200 行→建議拆子 View
2. body 內不可有副作用；onAppear/task 職責分離
3. 檢查 @Published 觀察風暴（每層都 ObservableObject）
4. 輸出結構化審查報告
EOF
cat > ~/.hermes/skills/capacitor-build/SKILL.md <<'EOF'
---
name: capacitor-build
description: Capacitor 跨平台打包：Web→iOS/Android 原生殼整合流程
---
## Procedure
1. `npm i @capacitor/core @capacitor/cli`；`npx cap init`
2. `npm run build && npx cap sync`
3. `npx cap open android` / `ios`
4. 外掛衝突→檢查 capacitor.config.ts 與 android/app/build.gradle
EOF
cat > ~/.hermes/skills/fastlane-release/SKILL.md <<'EOF'
---
name: fastlane-release
description: fastlane 自動化發版：match 憑證、pilot 送審、supply 上架
---
## Procedure
1. `gem install fastlane`；`fastlane init`
2. iOS：`fastlane match appstore` + `fastlane release`
3. Android：`fastlane supply init` 取 metadata
4. 失敗→看 fastlane 日錄 + 憑證到期檢查
EOF
```

**35-38｜APK 逆向 / iOS 建置 / Gradle 調優 / 依賴稽核**
```bash
mkdir -p ~/.hermes/skills/{reverse-apk,ios-build-xcconfig,gradle-optimize,dependency-audit}
cat > ~/.hermes/skills/reverse-apk/SKILL.md <<'EOF'
---
name: reverse-apk
description: 授權範圍內 APK 靜態分析：jadx/apktool 流程、敏感資訊洩漏檢查
---
## Procedure
1. `jadx -d out app.apk` 反編譯；`apktool d app.apk` 取資源
2. grep 硬編碼金鑰、API endpoint、exported component
3. AndroidManifest 權限與 intent-filter 審查
4. 輸出：風險清單 + 證據截圖路徑
EOF
cat > ~/.hermes/skills/ios-build-xcconfig/SKILL.md <<'EOF'
---
name: ios-build-xcconfig
description: iOS 建構設定管理：xcconfig 分層、Build Setting 衝突排查
---
## Procedure
1. 以 xcconfig 分環境（Debug/Release/AppStore）
2. `xcodebuild -workspace X.xcworkspace -scheme Y -configuration Release build`
3. 衝突→`xcodebuild -showBuildSettings` 對照
4. 產出 .ipa 並驗證簽章
EOF
cat > ~/.hermes/skills/gradle-optimize/SKILL.md <<'EOF'
---
name: gradle-optimize
description: Gradle 建構加速與依賴管理：快取、平行、版本對齊
---
## Procedure
1. 啟用 org.gradle.caching=true、parallel=true
2. `gradlew build --scan` 分析瓶頸 task
3. 依賴對齊：統一 BOM；排除重複函式庫
4. CI 快取目錄設定
EOF
cat > ~/.hermes/skills/dependency-audit/SKILL.md <<'EOF'
---
name: dependency-audit
description: 依賴供應鏈檢查：pip-audit/npm audit/OSV 掃描與修復
---
## Procedure
1. Python：`pip-audit`；Node：`npm audit --json`
2. OSV：`pip install osv-scanner && osv-scanner -r .`
3. 產生 CVE 清單：嚴重度、影響路徑、修復版本
4. 鎖定檔更新與回歸測試
EOF
```

**39-42｜安全程式碼審查 / 威脅建模 / Prompt-injection 授權測試 / garak 執行**
```bash
mkdir -p ~/.hermes/skills/{secure-code-review,threat-model,prompt-injection-test,garak-runner}
cat > ~/.hermes/skills/secure-code-review/SKILL.md <<'EOF'
---
name: secure-code-review
description: OWASP Top 10 導向程式碼審查（注入、SSRF、反序列化、權限）
---
## Procedure
1. 盤點輸入入口（HTTP、檔案、環境變數）
2. 追蹤到 sink（SQL、exec、eval、模板渲染）
3. 標註 CWE 編號與可利用路徑
4. 輸出嚴重度分級 + 修復 patch 建議
EOF
cat > ~/.hermes/skills/threat-model/SKILL.md <<'EOF'
---
name: threat-model
description: STRIDE 威脅建模：資料流圖、信任邊界、威脅列舉
---
## Procedure
1. 畫 DFD（外部實體、程序、資料儲存、資料流）
2. 標信任邊界；對每個元素跑 STRIDE
3. 產出威脅清單 + 緩解措施 + 優先級
EOF
cat > ~/.hermes/skills/prompt-injection-test/SKILL.md <<'EOF'
---
name: prompt-injection-test
description: 對自己部署的本地模型做提示注入韌性測試（僅限授權標的）
---
## Procedure
1. 標的：自己擁有的端點；取得書面授權
2. 變體：直接注入、間接注入（文件/網頁內嵌）、越權指令
3. 記錄：是否執行未授權動作、資料外洩跡象
4. 產出：韌性報告 + 緩解（輸入過濾、工具白名單）
EOF
cat > ~/.hermes/skills/garak-runner/SKILL.md <<'EOF'
---
name: garak-runner
description: 以 garak 對自有 LLM 端點做紅隊探測（越獄/ promptinject / 毒性）
---
## Procedure
1. `pip install garak`
2. `python -m garak --model_type openai --generator_options '{"base_url":"http://你的端點/v1"}' --probes promptinject`
3. 其他探針：jailbreak、dan、encoding、malwaregen
4. 輸出 HTML 報告，彙總 fail 項目與緩解
EOF
```

**43-46｜promptfoo / SAST / 機密衛生 / Docker 強化**
```bash
mkdir -p ~/.hermes/skills/{promptfoo-suite,sast-scan,secrets-hygiene,docker-hardening}
cat > ~/.hermes/skills/promptfoo-suite/SKILL.md <<'EOF'
---
name: promptfoo-suite
description: promptfoo 評測：斷言、紅隊變體、回歸測試整合 CI
---
## Procedure
1. `npm i -g promptfoo`
2. 寫 promptfooconfig.yaml：providers、prompts、tests（assert 斷言）
3. `promptfoo eval`；紅隊：`promptfoo redteam init`
4. CI：`promptfoo eval --output results.json`
EOF
cat > ~/.hermes/skills/sast-scan/SKILL.md <<'EOF'
---
name: sast-scan
description: Semgrep/CodeQL 靜態掃描流程與誤報分流
---
## Procedure
1. `pip install semgrep && semgrep --config auto .`
2. CodeQL：`codeql database create db --language=python && codeql analyze db`
3. 分級：真陽性修復、誤報標註
4. 產出 SARIF 供 GitHub Code Scanning
EOF
cat > ~/.hermes/skills/secrets-hygiene/SKILL.md <<'EOF'
---
name: secrets-hygiene
description: 機密衛生：gitleaks 掃描、pre-commit 攔截、洩漏後處置
---
## Procedure
1. `gitleaks detect --source . -v`
2. 加 pre-commit hook 阻擋新洩漏
3. 已洩漏→撤銷金鑰 > 清除 git 歷史 > 輪替
EOF
cat > ~/.hermes/skills/docker-hardening/SKILL.md <<'EOF'
---
name: docker-hardening
description: 容器強化：精簡基底、非 root、唯讀檔系統、cap drop
---
## Procedure
1. 基底：distroless/alpine；多階段建構
2. USER 非 root；read_only、no-new-privileges
3. 掃描：`docker scout cves` 或 trivy
4. 輸出 hardened Dockerfile 差異
EOF
```

**47-50｜K8s 健康 / Terraform / SQL 審查 / API 設計**
```bash
mkdir -p ~/.hermes/skills/{k8s-health,terraform-check,sql-review,api-design-review}
cat > ~/.hermes/skills/k8s-health/SKILL.md <<'EOF'
---
name: k8s-health
description: Kubernetes 集群健康檢查 runbook
---
## Procedure
1. `kubectl get nodes` 找 NotReady
2. `kubectl top nodes` 資源壓力
3. CrashLoopBackOff：`kubectl logs --previous`、describe 看事件
4. 輸出結構化報告 + 修復命令
EOF
cat > ~/.hermes/skills/terraform-check/SKILL.md <<'EOF'
---
name: terraform-check
description: Terraform/IaC 驗證：fmt、validate、plan 審查、tfsec
---
## Procedure
1. `terraform fmt -check && terraform validate`
2. `terraform plan -out plan.tfplan` 人工審 diff
3. `tfsec .` 安全掃描
4. 變更風險分級後 apply
EOF
cat > ~/.hermes/skills/sql-review/SKILL.md <<'EOF'
---
name: sql-review
description: SQL 審查：執行計畫、索引建議、慢查詢改造
---
## Procedure
1. EXPLAIN ANALYZE 取計畫
2. 全表掃描→複合索引；N+1→重寫 JOIN/批次
3. 邊界：分頁深度、大交易拆分
EOF
cat > ~/.hermes/skills/api-design-review/SKILL.md <<'EOF'
---
name: api-design-review
description: REST/GraphQL API 設計審查：資源命名、版本策略、錯誤格式
---
## Procedure
1. 檢查一致命名、HTTP 動詞語義
2. 分頁/過濾/排序標準化
3. 錯誤格式 RFC 7807；版本策略
4. OpenAPI 規格完整性
EOF
```

**51-54｜測試策略 / TDD / 重構計畫 / 文件同步**
```bash
mkdir -p ~/.hermes/skills/{test-strategy,tdd-loop,refactor-plan,doc-sync}
cat > ~/.hermes/skills/test-strategy/SKILL.md <<'EOF'
---
name: test-strategy
description: 測試策略設計：金字塔、覆蓋率目標、關鍵路徑優先
---
## Procedure
1. 畫模組依賴圖，標高風險路徑
2. 單測/整合/E2E 比例與工具選型
3. 定義覆蓋率門檻與 CI gate
EOF
cat > ~/.hermes/skills/tdd-loop/SKILL.md <<'EOF'
---
name: tdd-loop
description: 紅綠重構循環：失敗測試→最小實作→重構
---
## Procedure
1. 寫一個會失敗的測試
2. 最小代碼通過
3. 重構並保持綠燈
4. 每輪提交粒度控制
EOF
cat > ~/.hermes/skills/refactor-plan/SKILL.md <<'EOF'
---
name: refactor-plan
description: 大型重構計畫：特性開關、分階段遷移、回滾點
---
## Procedure
1. 圈定範圍與不可變行為（characterization tests）
2. 分階段：每階段可獨立交付
3. 特性開關 + 灰度
4. 回滾劇本
EOF
cat > ~/.hermes/skills/doc-sync/SKILL.md <<'EOF'
---
name: doc-sync
description: 程式與文件同步檢查：README/API 文件/變更日誌一致性
---
## Procedure
1. 比對最近 commit 與文件陳述
2. 標註過期段落
3. 產出更新 patch
EOF
```

**55-58｜PR 描述 / Commit 衛生 / 嚴格 code review / 效能分析**
```bash
mkdir -p ~/.hermes/skills/{pr-description,commit-hygiene,code-review-rigor,perf-profiling}
cat > ~/.hermes/skills/pr-description/SKILL.md <<'EOF'
---
name: pr-description
description: 高品質 PR 描述：動機、方案、測試證據、回滾計畫
---
## Procedure
1. 標題 < 72 字，動詞開頭
2. 內文：Why/What/How tested/Rollback
3. 關聯 issue；截圖/GIF 證據
EOF
cat > ~/.hermes/skills/commit-hygiene/SKILL.md <<'EOF'
---
name: commit-hygiene
description: Commit 規範：conventional commits、原子提交、訊息品質
---
## Procedure
1. 格式：type(scope): subject
2. 一個 commit 只做一件事
3. 訊息寫「為什麼」而非「做了什麼」
EOF
cat > ~/.hermes/skills/code-review-rigor/SKILL.md <<'EOF'
---
name: code-review-rigor
description: 嚴格 code review：資料結構、簡潔性、安全性、風險
---
## Procedure
1. 先讀測試再讀實作
2. 檢查邊界條件與錯誤處理
3. 安全視角：注入、權限、日誌洩漏
4. 回報格式：block/major/minor/nit
EOF
cat > ~/.hermes/skills/perf-profiling/SKILL.md <<'EOF'
---
name: perf-profiling
description: 效能分析：CPU/記憶體/IO 剖析工具選用與瓶頸定位
---
## Procedure
1. Python：cProfile/py-spy；Node：clinic/0x；Go：pprof
2. 火焰圖解讀：寬=耗時
3. 產出：瓶頸排名 + 優化方案 + 基準前後對比
EOF
```

**59-62｜研究簡報 / Repo 上手 / CI 除錯 / 發佈檢查清單**
```bash
mkdir -p ~/.hermes/skills/{research-brief,repo-onboarding,ci-debug,release-checklist}
cat > ~/.hermes/skills/research-brief/SKILL.md <<'EOF'
---
name: research-brief
description: 主題研究簡報：來源評級、交叉驗證、摘要產出
---
## Procedure
1. 多來源蒐集（官方文件 > 原始論文 > 次級來源）
2. 交叉驗證矛盾點
3. 輸出：摘要、關鍵數據、來源清單、可信度評級
EOF
cat > ~/.hermes/skills/repo-onboarding/SKILL.md <<'EOF'
---
name: repo-onboarding
description: 新 repo 快速上手：架構圖、建置指令、測試入口、除錯入口
---
## Procedure
1. 讀 README/Makefile/package.json 建立建置心智模型
2. 追蹤 main 入口到核心模組
3. 產出：onboarding 筆記 + 首個可跑範例
EOF
cat > ~/.hermes/skills/ci-debug/SKILL.md <<'EOF'
---
name: ci-debug
description: CI 失敗排查：本機復現、日誌分段、快取問題
---
## Procedure
1. 本地執行相同命令復現
2. 分段日誌定位第一個紅燈
3. 檢查 runner 環境差異（OS/版本/金鑰）
EOF
cat > ~/.hermes/skills/release-checklist/SKILL.md <<'EOF'
---
name: release-checklist
description: 發佈檢查清單：版本號、changelog、標籤、artifact 驗證
---
## Procedure
1. 版本號語義化；changelog 完整
2. 建立 signed tag
3. 建構 artifact 並校驗雜湊
4. 發佈後驗證安裝路徑
EOF
```

**63-66｜事件分診 / 日誌分析 / git bisect / 合併衝突**
```bash
mkdir -p ~/.hermes/skills/{incident-triage,log-analysis,git-bisect-guide,merge-conflict}
cat > ~/.hermes/skills/incident-triage/SKILL.md <<'EOF'
---
name: incident-triage
description: 事件分診：影響面、時間線、假設排序、止血動作
---
## Procedure
1. 定義影響面（用戶數、功能面）
2. 拉時間線：deploy→告警→復原
3. 假設排序（最可能×最快驗證）
4. 先止血再根治
EOF
cat > ~/.hermes/skills/log-analysis/SKILL.md <<'EOF'
---
name: log-analysis
description: 分散日誌分析：grep/awk 模式、異常聚類、關聯 ID 追蹤
---
## Procedure
1. 以 request-id 串全鏈路
2. 統計異常碼分布找聚類
3. 輸出：時間線 + 根因候選
EOF
cat > ~/.hermes/skills/git-bisect-guide/SKILL.md <<'EOF'
---
name: git-bisect-guide
description: git bisect 二分定位引入問題的 commit
---
## Procedure
1. `git bisect start`；標記 good/bad
2. 自動腳本：`git bisect run ./test.sh`
3. 收斂後 `git bisect reset`，分析該 commit
EOF
cat > ~/.hermes/skills/merge-conflict/SKILL.md <<'EOF'
---
name: merge-conflict
description: 合併衝突解決策略：三方比對、保留語意、驗證
---
## Procedure
1. `git mergetool` 三方檢視
2. 理解雙方意圖再合併，非機械取一邊
3. 解完跑測試驗證
EOF
```

**67-70｜Monorepo / API client 生成 / DB migration / 記憶維護**
```bash
mkdir -p ~/.hermes/skills/{monorepo-nav,api-client-gen,db-migration,skill-authoring}
cat > ~/.hermes/skills/monorepo-nav/SKILL.md <<'EOF'
---
name: monorepo-nav
description: Monorepo 導航：workspace 拓撲、依賴圖、影響範圍分析
---
## Procedure
1. 盤點 packages/apps 結構
2. 建依賴圖；改動→影響範圍
3. 建置快取策略建議
EOF
cat > ~/.hermes/skills/api-client-gen/SKILL.md <<'EOF'
---
name: api-client-gen
description: 由 OpenAPI 產生型別安全 client（openapi-typescript / orval）
---
## Procedure
1. `npx openapi-typescript spec.yaml -o schema.ts`
2. 或 `npx orval` 產生 hooks client
3. 驗證型別與 runtime 行為一致
EOF
cat > ~/.hermes/skills/db-migration/SKILL.md <<'EOF'
---
name: db-migration
description: 資料庫遷移：擴張收縮法、零停機、回滾演練
---
## Procedure
1. 新欄位先加後用；舊欄位先停寫再刪
2. 大表：分批 backfill + 進度追蹤
3. 遷移前後資料量校驗
EOF
cat > ~/.hermes/skills/skill-authoring/SKILL.md <<'EOF'
---
name: skill-authoring
description: 撰寫高品質 Hermes SKILL.md：觸發精準、步驟可驗證
---
## Procedure
1. description 寫「何時用」而非「是什麼」
2. Procedure 每步可機械執行
3. 收尾定義產出格式
EOF
```


---

# 二、DeepSeek Harness（DSH）— 70 項

DSH 是 DeepSeek AI 2026-08 開源的 agent harness（MIT），核心理念「Everything is a Plugin」：模型、工具、技能、session、沙箱、agent loop 全是可替換的外掛。開發者預覽版，迭代快。套件來源：官方倉庫、`dsh-external/hub` 目錄、GitHub `dsh-plugin` topic（本清單逐條取自官方 awesome 目錄，2026-09）。

## 2-1. 核心執行環境（6 項）

**01｜官方 npx 一鍵（含 Web UI）**
```bash
npx @deepseek-ai/dsh web
```

**02｜原始碼安裝**
```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

**03｜外掛安裝語法（GitHub/本機/npm spec 皆可）**
```bash
dsh plugin --profile web add "github:owner/repo#ref"
dsh plugin add <npm-套件名>
# 管理介面：Web UI → Settings → Plugins
```

**04｜Windows 桌面啟動器（零命令列視窗）**
```bash
npm i -g dsh-desktop-launcher
```

**05｜系統匣守護（Win）**
```bash
npm i -g dsh-tray
```

**06｜DSHBox — 直接在 Android 手機跑 DSH（Debian 沙箱 + Node + DSH，免 root 免 Termux）**
> 下載 APK：https://github.com/topics/dshbox 或搜尋「DSHBox」release 頁安裝

## 2-2. 多 Agent 協作與編排（14 項）

**07｜多 Agent 團隊編排**
```bash
dsh plugin --profile web add "github:NanmiCoder/dsh-agent-teams"
```
**08｜可靠待辦面板（三態驗證）** `dsh plugin add dsh-todo-guard`
**09｜任務管理引擎（Linear 式 issue store）** `dsh plugin add fakechris/dsh-track`
**10｜多 Agent 協作套件（team_call/team_message 等）** `dsh plugin add dsh-collaboration`
**11｜計畫優先預設（research→plan→verify）** `dsh plugin add dsh-plans`
**12｜多模型小隊 + DAG 執行** `dsh plugin add dsh-agent-team-gui`
**13｜執行紀律套件（重試攔截/反思/經驗轉技能）** `dsh plugin add cleverer-dsh`
**14｜平行 git worktree 蟲群** `dsh plugin add february2015/dsh-taskswarm`
**15｜批次平行子代理分派（swarm_batch）** `dsh plugin add hongyue0721/dsh-kimicode-swarm`
**16｜自進化引擎（外掛候選自動評測收錄）** `dsh plugin add timwhitez/dsh-self-evolving`
**17｜模型高可用容錯 + 子代理編排** `dsh plugin add Saktawdi/dsh-ha-orchestrator`
**18｜常駐背景子代理** `dsh plugin add dsh-background-agents`
**19｜跨 session 團隊房間** `dsh plugin add dsh-team-rooms`
**20｜單發子代理（可掛任意 preset/外部 CLI）** `dsh plugin add bpc-oss/dsh-routed-subagent`

## 2-3. Context / 搜尋 / 記憶（12 項）

**21｜Context 洞察面板** `dsh plugin add dsh-context`
**22｜工具輸出壓縮（省 context）** `dsh plugin add dsh-compressor`
**23｜Context 即時圓環圖** `dsh plugin add context-vista`
**24｜Context 健檢（AGENTS.md/技能/工具 token 成本）** `dsh plugin add dsh-context-doctor`
**25｜增量檔案掛載（不重送已讀行）** `dsh plugin add dsh-file-mount`
**26｜多引擎增強搜尋（含 GitHub/YouTube/Reddit）** `dsh plugin add dsh-web-search-pro`
**27｜免費網搜（10 引擎 fallback）** `dsh plugin add dsh-free-web-search`
**28｜大型 MCP 工具目錄漸進式閘道** `dsh plugin add dsh-mcp-lens`
**29｜跨 session 長期記憶引擎（SQLite+離線語意搜尋）** `dsh plugin add dsh-mneme`
**30｜分層長期記憶（USER.md+MEMORY.md+Fibonacci 上限）** `dsh plugin add dsh-hme`
**31｜記憶保險庫（remember/recall/forget）** `dsh plugin add dsh-memory-vault`
**32｜共用 Markdown 記憶（自動擷取注入）** `dsh plugin add zilliztech/memsearch`

## 2-4. Git / 工程協作（12 項）

**33｜結構化 Git 工具（含破壞指令防護）** `dsh plugin add dsh-tool-git`
**34｜Git 狀態抽屜（commit DAG 圖）** `dsh plugin add dsh-git-status`
**35｜測試執行器（auto-detect Vitest/Jest/pytest）** `dsh plugin add dsh-test-runner`
**36｜LSP 動作（診斷/重構/補全/改名）** `dsh plugin add dsh-lsp-actions`
**37｜Codex 式 diff 審查浮窗（stage/commit/push）** `dsh plugin add dsh-plugin-diff-review`
**38｜快照回捲（git-first /rewind）** `dsh plugin add dsh-checkpoint-rewind`
**39｜增量 diff 審查循環** `dsh plugin add dsh-review-loop`
**40｜工程紀律環（需求質問+紅綠證據+對抗審查）** `dsh plugin add dsh-doublecheck`
**41｜規格驅動開發技能包（Keel 龍骨）** `dsh plugin --profile web add "github:JohnXu22786/spec-driven"`
**42｜全端工程工作流（垂直切片規畫+證據檢查）** `dsh plugin add dsh-fullstack-expert`
**43｜GitHub Action（PR 審查/CI 診斷/issue→PR）** `dsh plugin --profile web add "github:deepseek-harness-action"`
**44｜任務隔離 git worktree** `dsh plugin --profile web add "github:JohnXu22786/worktree-mgr"`

## 2-5. 手機/行動開發（8 項）

**45｜ADB 裝置操作（logcat/apk 安裝/效能快照）** `dsh plugin add dsh-adb`
**46｜DSHBox（Android APK，見 06）** — 與 45 搭配在手機上開發
**47｜手機 client 外掛** `dsh plugin add dsh-mobile`
**48｜行動版/PWA 版面適配 + LAN WebSocket 修正** `dsh plugin add dsh-mobileweb-adapter`
**49｜手機派工指揮中心（PWA + E2E 加密中繼）** `dsh plugin add dsh-dispatch`
**50｜第三方手機遠端 client（LAN/QR 連線）** 搜尋安裝 `harness-remote`
**51｜SSH 多主機遠端工作區** `dsh plugin add dsh-remote`
**52｜LAN 存取綁定 + 金鑰登入閘道** `dsh plugin --profile web add "github:xgone/dsh-remote"`

## 2-6. 安全 / 紅隊 / 防護（10 項）

**53｜提示注入/越獄/金鑰洩漏偵測閘門（Aho-Corasick 規則庫）** `dsh plugin add dsh-defend`
**54｜外掛安裝前靜態稽核（dsh-vet/v1 報告）** `dsh plugin add dsh-vet`
**55｜供應鏈毒化掃描（JS-X-Ray 反混淆）** `dsh plugin add zoahdev/dsh-poison-guard`
**56｜金鑰去汙（工具輸出/日誌遮罩）** `dsh plugin add dsh-secret-scrub`
**57｜執行前護欄（危險指令否決）** `dsh plugin add dsh-safeguard`
**58｜宣告式 allow/deny/ask 權限規則** `dsh plugin add dsh-permission-rules`
**59｜PII 遮罩中介層** `dsh plugin add dsh-mask`
**60｜機密檔案存取封鎖 + 稽核** `dsh plugin --profile web add "github:JohnXu22786/secret-guard"`
**61｜破壞指令攔截（rm -rf / push --force）** `dsh plugin --profile web add "github:JohnXu22786/safety-net"`
**62｜加密憑證庫（AES-256-GCM + Argon2id）** `dsh plugin add dsh-encrypt`

## 2-7. 市場 / 管理 / IDE / 觀測（8 項）

**63｜外掛中心（一鍵裝卸、500+ 外掛索引）** `dsh plugin add dsh-plugin-hub`
**64｜設定備份/匯出/遷移（整包 ZIP）** `dsh plugin add dsh-config-manager`
**65｜一鍵備份還原 ~/.dsh** `dsh plugin add dsh-backup`
**66｜環境健檢（node/pnpm/金鑰/工作區）** `dsh plugin add zoahdev/dsh-firstrun`
**67｜VS Code 側欄 client（diff 審查/審批卡）** 安裝 `dsh-vscode` 擴充
**68｜用量/成本儀表板（官方計費、峰谷電價）** `dsh plugin add dsh-usage`
**69｜OTel GenAI tracing（span tree per turn）** `dsh plugin add loongsuite/dsh-plugin`
**70｜事件/事件流稽核面板** `dsh plugin add dsh-event-auditor`

> 加碼推薦（同目錄可查）：`dsh-claude-move`（Claude Code/Codex/Hermes 遷移精靈）、`dsh-skill-mover`（14 平台技能搬遷）、`dsh-movein`、`hermes-dsh-collab`（Hermes×DSH 協作）、`dsh-eval`（評測平台）。


---

2. 追蹤 main 入口到核心模組
3. 產出：onboarding 筆記 + 首個可跑範例
EOF
cat > ~/.hermes/skills/ci-debug/SKILL.md <<'EOF'
---
name: ci-debug
description: CI 失敗排查：本機復現、日誌分段、快取問題
---
## Procedure
1. 本地執行相同命令復現
2. 分段日誌定位第一個紅燈
3. 檢查 runner 環境差異（OS/版本/金鑰）
EOF
cat > ~/.hermes/skills/release-checklist/SKILL.md <<'EOF'
---
name: release-checklist
description: 發佈檢查清單：版本號、changelog、標籤、artifact 驗證
---
## Procedure
1. 版本號語義化；changelog 完整
2. 建立 signed tag
3. 建構 artifact 並校驗雜湊
4. 發佈後驗證安裝路徑
EOF
```

**63-66｜事件分診 / 日誌分析 / git bisect / 合併衝突**
```bash
mkdir -p ~/.hermes/skills/{incident-triage,log-analysis,git-bisect-guide,merge-conflict}
cat > ~/.hermes/skills/incident-triage/SKILL.md <<'EOF'
---
name: incident-triage
description: 事件分診：影響面、時間線、假設排序、止血動作
---
## Procedure
1. 定義影響面（用戶數、功能面）
2. 拉時間線：deploy→告警→復原
3. 假設排序（最可能×最快驗證）
4. 先止血再根治
EOF
cat > ~/.hermes/skills/log-analysis/SKILL.md <<'EOF'
---
name: log-analysis
description: 分散日誌分析：grep/awk 模式、異常聚類、關聯 ID 追蹤
---
## Procedure
1. 以 request-id 串全鏈路
2. 統計異常碼分布找聚類
3. 輸出：時間線 + 根因候選
EOF
cat > ~/.hermes/skills/git-bisect-guide/SKILL.md <<'EOF'
---
name: git-bisect-guide
description: git bisect 二分定位引入問題的 commit
---
## Procedure
1. `git bisect start`；標記 good/bad
2. 自動腳本：`git bisect run ./test.sh`
3. 收斂後 `git bisect reset`，分析該 commit
EOF
cat > ~/.hermes/skills/merge-conflict/SKILL.md <<'EOF'
---
name: merge-conflict
description: 合併衝突解決策略：三方比對、保留語意、驗證
---
## Procedure
1. `git mergetool` 三方檢視
2. 理解雙方意圖再合併，非機械取一邊
3. 解完跑測試驗證
EOF
```

**67-70｜Monorepo / API client 生成 / DB migration / 記憶維護**
```bash
mkdir -p ~/.hermes/skills/{monorepo-nav,api-client-gen,db-migration,skill-authoring}
cat > ~/.hermes/skills/monorepo-nav/SKILL.md <<'EOF'
---
name: monorepo-nav
description: Monorepo 導航：workspace 拓撲、依賴圖、影響範圍分析
---
## Procedure
1. 盤點 packages/apps 結構
2. 建依賴圖；改動→影響範圍
3. 建置快取策略建議
EOF
cat > ~/.hermes/skills/api-client-gen/SKILL.md <<'EOF'
---
name: api-client-gen
description: 由 OpenAPI 產生型別安全 client（openapi-typescript / orval）
---
## Procedure
1. `npx openapi-typescript spec.yaml -o schema.ts`
2. 或 `npx orval` 產生 hooks client
3. 驗證型別與 runtime 行為一致
EOF
cat > ~/.hermes/skills/db-migration/SKILL.md <<'EOF'
---
name: db-migration
description: 資料庫遷移：擴張收縮法、零停機、回滾演練
---
## Procedure
1. 新欄位先加後用；舊欄位先停寫再刪
2. 大表：分批 backfill + 進度追蹤
3. 遷移前後資料量校驗
EOF
cat > ~/.hermes/skills/skill-authoring/SKILL.md <<'EOF'
---
name: skill-authoring
description: 撰寫高品質 Hermes SKILL.md：觸發精準、步驟可驗證
---
## Procedure
1. description 寫「何時用」而非「是什麼」
2. Procedure 每步可機械執行
3. 收尾定義產出格式
EOF
```


---

# 二、DeepSeek Harness（DSH）— 70 項

DSH 是 DeepSeek AI 2026-08 開源的 agent harness（MIT），核心理念「Everything is a Plugin」：模型、工具、技能、session、沙箱、agent loop 全是可替換的外掛。開發者預覽版，迭代快。套件來源：官方倉庫、`dsh-external/hub` 目錄、GitHub `dsh-plugin` topic（本清單逐條取自官方 awesome 目錄，2026-09）。

## 2-1. 核心執行環境（6 項）

**01｜官方 npx 一鍵（含 Web UI）**
```bash
npx @deepseek-ai/dsh web
```

**02｜原始碼安裝**
```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

**03｜外掛安裝語法（GitHub/本機/npm spec 皆可）**
```bash
dsh plugin --profile web add "github:owner/repo#ref"
dsh plugin add <npm-套件名>
# 管理介面：Web UI → Settings → Plugins
```

**04｜Windows 桌面啟動器（零命令列視窗）**
```bash
npm i -g dsh-desktop-launcher
```

**05｜系統匣守護（Win）**
```bash
npm i -g dsh-tray
```

**06｜DSHBox — 直接在 Android 手機跑 DSH（Debian 沙箱 + Node + DSH，免 root 免 Termux）**
> 下載 APK：https://github.com/topics/dshbox 或搜尋「DSHBox」release 頁安裝

## 2-2. 多 Agent 協作與編排（14 項）

**07｜多 Agent 團隊編排**
```bash
dsh plugin --profile web add "github:NanmiCoder/dsh-agent-teams"
```
**08｜可靠待辦面板（三態驗證）** `dsh plugin add dsh-todo-guard`
**09｜任務管理引擎（Linear 式 issue store）** `dsh plugin add fakechris/dsh-track`
**10｜多 Agent 協作套件（team_call/team_message 等）** `dsh plugin add dsh-collaboration`
**11｜計畫優先預設（research→plan→verify）** `dsh plugin add dsh-plans`
**12｜多模型小隊 + DAG 執行** `dsh plugin add dsh-agent-team-gui`
**13｜執行紀律套件（重試攔截/反思/經驗轉技能）** `dsh plugin add cleverer-dsh`
**14｜平行 git worktree 蟲群** `dsh plugin add february2015/dsh-taskswarm`
**15｜批次平行子代理分派（swarm_batch）** `dsh plugin add hongyue0721/dsh-kimicode-swarm`
**16｜自進化引擎（外掛候選自動評測收錄）** `dsh plugin add timwhitez/dsh-self-evolving`
**17｜模型高可用容錯 + 子代理編排** `dsh plugin add Saktawdi/dsh-ha-orchestrator`
**18｜常駐背景子代理** `dsh plugin add dsh-background-agents`
**19｜跨 session 團隊房間** `dsh plugin add dsh-team-rooms`
**20｜單發子代理（可掛任意 preset/外部 CLI）** `dsh plugin add bpc-oss/dsh-routed-subagent`

## 2-3. Context / 搜尋 / 記憶（12 項）

**21｜Context 洞察面板** `dsh plugin add dsh-context`
**22｜工具輸出壓縮（省 context）** `dsh plugin add dsh-compressor`
**23｜Context 即時圓環圖** `dsh plugin add context-vista`
**24｜Context 健檢（AGENTS.md/技能/工具 token 成本）** `dsh plugin add dsh-context-doctor`
**25｜增量檔案掛載（不重送已讀行）** `dsh plugin add dsh-file-mount`
**26｜多引擎增強搜尋（含 GitHub/YouTube/Reddit）** `dsh plugin add dsh-web-search-pro`
**27｜免費網搜（10 引擎 fallback）** `dsh plugin add dsh-free-web-search`
**28｜大型 MCP 工具目錄漸進式閘道** `dsh plugin add dsh-mcp-lens`
**29｜跨 session 長期記憶引擎（SQLite+離線語意搜尋）** `dsh plugin add dsh-mneme`
**30｜分層長期記憶（USER.md+MEMORY.md+Fibonacci 上限）** `dsh plugin add dsh-hme`
**31｜記憶保險庫（remember/recall/forget）** `dsh plugin add dsh-memory-vault`
**32｜共用 Markdown 記憶（自動擷取注入）** `dsh plugin add zilliztech/memsearch`

## 2-4. Git / 工程協作（12 項）

**33｜結構化 Git 工具（含破壞指令防護）** `dsh plugin add dsh-tool-git`
**34｜Git 狀態抽屜（commit DAG 圖）** `dsh plugin add dsh-git-status`
**35｜測試執行器（auto-detect Vitest/Jest/pytest）** `dsh plugin add dsh-test-runner`
**36｜LSP 動作（診斷/重構/補全/改名）** `dsh plugin add dsh-lsp-actions`
**37｜Codex 式 diff 審查浮窗（stage/commit/push）** `dsh plugin add dsh-plugin-diff-review`
**38｜快照回捲（git-first /rewind）** `dsh plugin add dsh-checkpoint-rewind`
**39｜增量 diff 審查循環** `dsh plugin add dsh-review-loop`
**40｜工程紀律環（需求質問+紅綠證據+對抗審查）** `dsh plugin add dsh-doublecheck`
**41｜規格驅動開發技能包（Keel 龍骨）** `dsh plugin --profile web add "github:JohnXu22786/spec-driven"`
**42｜全端工程工作流（垂直切片規畫+證據檢查）** `dsh plugin add dsh-fullstack-expert`
**43｜GitHub Action（PR 審查/CI 診斷/issue→PR）** `dsh plugin --profile web add "github:deepseek-harness-action"`
**44｜任務隔離 git worktree** `dsh plugin --profile web add "github:JohnXu22786/worktree-mgr"`

## 2-5. 手機/行動開發（8 項）

**45｜ADB 裝置操作（logcat/apk 安裝/效能快照）** `dsh plugin add dsh-adb`
**46｜DSHBox（Android APK，見 06）** — 與 45 搭配在手機上開發
**47｜手機 client 外掛** `dsh plugin add dsh-mobile`
**48｜行動版/PWA 版面適配 + LAN WebSocket 修正** `dsh plugin add dsh-mobileweb-adapter`
**49｜手機派工指揮中心（PWA + E2E 加密中繼）** `dsh plugin add dsh-dispatch`
**50｜第三方手機遠端 client（LAN/QR 連線）** 搜尋安裝 `harness-remote`
**51｜SSH 多主機遠端工作區** `dsh plugin add dsh-remote`
**52｜LAN 存取綁定 + 金鑰登入閘道** `dsh plugin --profile web add "github:xgone/dsh-remote"`

## 2-6. 安全 / 紅隊 / 防護（10 項）

**53｜提示注入/越獄/金鑰洩漏偵測閘門（Aho-Corasick 規則庫）** `dsh plugin add dsh-defend`
**54｜外掛安裝前靜態稽核（dsh-vet/v1 報告）** `dsh plugin add dsh-vet`
**55｜供應鏈毒化掃描（JS-X-Ray 反混淆）** `dsh plugin add zoahdev/dsh-poison-guard`
**56｜金鑰去汙（工具輸出/日誌遮罩）** `dsh plugin add dsh-secret-scrub`
**57｜執行前護欄（危險指令否決）** `dsh plugin add dsh-safeguard`
**58｜宣告式 allow/deny/ask 權限規則** `dsh plugin add dsh-permission-rules`
**59｜PII 遮罩中介層** `dsh plugin add dsh-mask`
**60｜機密檔案存取封鎖 + 稽核** `dsh plugin --profile web add "github:JohnXu22786/secret-guard"`
**61｜破壞指令攔截（rm -rf / push --force）** `dsh plugin --profile web add "github:JohnXu22786/safety-net"`
**62｜加密憑證庫（AES-256-GCM + Argon2id）** `dsh plugin add dsh-encrypt`

## 2-7. 市場 / 管理 / IDE / 觀測（8 項）

**63｜外掛中心（一鍵裝卸、500+ 外掛索引）** `dsh plugin add dsh-plugin-hub`
**64｜設定備份/匯出/遷移（整包 ZIP）** `dsh plugin add dsh-config-manager`
**65｜一鍵備份還原 ~/.dsh** `dsh plugin add dsh-backup`
**66｜環境健檢（node/pnpm/金鑰/工作區）** `dsh plugin add zoahdev/dsh-firstrun`
**67｜VS Code 側欄 client（diff 審查/審批卡）** 安裝 `dsh-vscode` 擴充
**68｜用量/成本儀表板（官方計費、峰谷電價）** `dsh plugin add dsh-usage`
**69｜OTel GenAI tracing（span tree per turn）** `dsh plugin add loongsuite/dsh-plugin`
**70｜事件/事件流稽核面板** `dsh plugin add dsh-event-auditor`

> 加碼推薦（同目錄可查）：`dsh-claude-move`（Claude Code/Codex/Hermes 遷移精靈）、`dsh-skill-mover`（14 平台技能搬遷）、`dsh-movein`、`hermes-dsh-collab`（Hermes×DSH 協作）、`dsh-eval`（評測平台）。


---

# 三、OpenWebUI — 70 項

OpenWebUI 的可掛載面：**Tools（給模型新能力）/ Functions（改變 WebUI 本身：Pipe、Filter、Action、Event）/ Skills（SKILL.md，模型可 view_skill 載入）/ MCP 工具伺服器 / 內建工具類別開關**。安裝主體：

**A0｜三種主體安裝（擇一）**
```bash
# PyPI
pip install open-webui
open-webui serve
# Docker（依你的要求省略 port 映射，請自行加上）
docker run -d -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
# Kubernetes
helm repo add open-webui https://helm.openwebui.com
helm install open-webui open-webui/open-webui
```

## 3-1. 內建能力開關（12 項，Admin → Settings → General 或 docker -e）

01｜Web Search：`ENABLE_WEB_SEARCH=true`、`WEB_SEARCH_ENGINE`（searxng/brave/google_pse/tavily/exa/duckduckgo/morph）
02｜混合檢索：`ENABLE_RAG_HYBRID_SEARCH=true`（內建工具 query_knowledge_files 走 hybrid+rerank）
03｜圖片生成：`ENABLE_IMAGE_GENERATION=true` + `IMAGE_GENERATION_ENGINE`（openai/comfyui/gemini）
04｜圖片編輯：`ENABLE_IMAGE_EDIT=true`
05｜沙箱程式執行：`ENABLE_CODE_INTERPRETER=true`（內建 execute_code 工具）
06｜頻道：`ENABLE_CHANNELS=true`（Teams/Slack/Discord 式頻道）
07｜筆記：`ENABLE_NOTES=true`
08｜KB 檔案系統介面：`ENABLE_KB_EXEC=true`（kb_exec：ls/tree/grep/cat 等）
09｜OAuth/OIDC：Google/GitHub/Microsoft/Authentik/Keycloak 登入開關
10｜LDAP 企業登入 + SMTP 郵件
11｜記憶體系統：Memory（個人化記憶）於 Admin 啟用，內建 add/search/update/delete 工具
12｜任務/行事曆/自動化內建工具：Task Management、Calendar、Automations（create/toggle/delete）

## 3-2. 社群函數庫 Tools & Functions（25 項，一鍵：Workspace → Tools / Admin → Functions → + → 從社群匯入，搜尋以下名稱）

13｜SearXNG Web Search（tool）— 免費自架搜尋
14｜Brave Web Search（tool）— 需 Brave API key
15｜Google Programmable Search（tool）
16｜Tavily Web Search（tool）— 附帶 extract
17｜Exa Web Search（tool）— 神經搜尋
18｜DuckDuckGo Search（tool）— 免 key
19｜Website RAG（tool）— 整站抓取而量產 embedding
20｜YouTube RAG（tool）— `docker exec open-webui pip install youtube-transcript-api`
21｜Memory / 長期記憶（function, filter）
22｜OpenAI Image Generation（pipe/manifold）
23｜ComfyUI Image Generation（pipe）— 接 ComfyUI 工作流
24｜Gemini Image Generation（pipe）
25｜DALL-E Manifold（pipe）— 多模型管理
26｜Function Calling（內建開關 + 社群增強版）
27｜Code Interpreter（內建 + 社群 Pyodide 版）
28｜Prompt Generation（function）— 自動潤飾 prompt
29｜Title Generation（function）— 對話命名
30｜LlamaIndex RAG（pipeline/legacy）：`pip install llama-index`
31｜Mem0 Memory（function）：`pip install mem0ai`
32｜Langfuse Filter（function，LLM 可觀測性）：`pip install langfuse`
33｜OpenTelemetry Filter：`pip install opentelemetry-sdk opentelemetry-exporter-otlp`
34｜Detoxify Filter（毒性內容過濾，紅隊必備）：`pip install detoxify`
35｜Rate Limit Filter（限速防刷）
36｜LibreTranslate Filter（即時翻譯）：接本地 libretranslate
37｜Inject Stats Filter（回應附帶 token 統計）

## 3-3. MCP 工具伺服器（12 項，Admin → Settings → External Tools 加入 MCP server）

```bash
# 常用 MCP server 啟動指令（於 OpenWebUI 的 MCP 設定中填寫）
38｜filesystem：npx -y @modelcontextprotocol/server-filesystem /允許目錄
39｜github：npx -y @modelcontextprotocol/server-github（需 GITHUB_TOKEN）
40｜gitlab：npx -y @modelcontextprotocol/server-gitlab
41｜postgres：npx -y @modelcontextprotocol/server-postgres 連線字串
42｜sqlite：npx -y @modelcontextprotocol/server-sqlite 資料庫路徑
43｜fetch：uvx mcp-server-fetch
44｜memory：npx -y @modelcontextprotocol/server-memory
45｜sequential-thinking：npx -y @modelcontextprotocol/server-sequential-thinking
46｜brave-search：npx -y @modelcontextprotocol/server-brave-search
47｜playwright：npx -y @playwright/mcp@latest（瀏覽器自動化）
48｜puppeteer：npx -y @modelcontextprotocol/server-puppeteer
49｜slack：npx -y @modelcontextprotocol/server-slack
```

## 3-4. Skills（10 顆，複製貼到 Workspace → Skills → 新增 → 貼上 frontmatter 內容）

50｜android-dev
```
---
name: android-dev
description: Android 開發輔助：Gradle 除錯、logcat 分析、Compose 審查。當使用者處理 Android 專案時使用。
---
1. 先判斷問題類型：建置/執行期/UI
2. 建置錯誤→執行 ./gradlew build 收錯誤堆疊
3. 執行期→adb logcat -b crash 定位
4. Compose 問題→檢查 recomposition 與狀態提升
5. 輸出：根因 + 最小修復 patch
```
51｜ios-dev（SwiftUI/SwiftData/Xcode 建置排查）
52｜flutter-dev（pub deps、EAS、OTA 更新流程）
53｜react-native-dev（Metro、原生模組、OTA）
54｜redteam-local-llm（對自有端點之 garak/promptfoo 授權測試流程）
55｜secure-code-review（OWASP 導向審查流程）
56｜api-design（REST/GraphQL 設計檢查清單）
57｜tdd-loop（紅綠重構紀律）
58｜release-checklist（語義化版本、changelog、artifact 校驗）
59｜ci-debug（CI 失敗本機復現流程）
60｜db-migration（零停機遷移擴張收縮法）

> 使用方式：Workspace → Models → 編輯模型 → Skills 勾選 → 模型獲得 view_skill 工具，按需載入全文，不佔 context。

## 3-5. 容器內補強與周邊（10 項）

61｜工具依賴批次安裝：
```bash
docker exec open-webui pip install youtube-transcript-api llama-index mem0ai langfuse detoxify duckduckgo-search tavily-python exa-py
```
62｜本機模型：安裝 Ollama 後於 Connections 加入（GPU 可用 open-webui 官方 cuda 映像檔）
63｜本地 TTS/STT：Admin → Audio 設定 OpenAI-compatible TTS（如 piper/localai）
64｜RAG embedding：Admin → Documents 設定本地 sentence-transformers 或 Ollama embedding
65｜向量庫外接：Chroma/Qdrant/Milvus/Pgvector/Weaviate 設定於 Admin → Documents
66｜Reranker：啟用 RAG rerank（FlashRank/Jina/Cohere）
67｜LiteLLM 代理：以 litellm 串接 100+ provider 後於 Connections 指向
68｜行動 PWA：手機瀏覽器「加到主畫面」即 App；或用社群 open-webui mobile app 專案
69｜備份：`docker cp open-webui:/app/backend/data ./backup`
70｜外網安全：啟用登入驗證 + OAuth + Rate Limit Filter（見 35）+ HTTPS 反向代理


---

# 四、OpenHands（原 OpenDevin，All Hands AI）— 60 項

OpenHands 的可掛載面：**Skills（SKILL.md，~/.openhands/skills 或 ~/.agents/skills 自動載入）/ Plugins（hooks+scripts）/ Extensions 公開註冊表（73 個：63 skills + 10 plugins）/ MCP 工具 / Automations 自動化**。SDK/CLI 支援 LLM via LiteLLM（100+ provider）。

## 4-1. 核心安裝（4 項）

**01｜pip 安裝（CLI + SDK）**
```bash
pip install openhands-ai
openhands
```
**02｜Docker 主體（依要求省略 port 映射）**
```bash
docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock -v $HOME/.openhands-state:/.openhands-state --name openhands all-hands-ai/openhands
```
**03｜GitHub Resolver（issue→PR 自動化 Action）**** — repo 加 `.github/workflows/openhands-resolver.yml`（官方範例於 OpenHands/OpenHands repo）
**04｜Extensions 註冊表全量 Skills 載入**
```bash
git clone --depth 1 https://github.com/openhands/extensions.git
mkdir -p ~/.openhands/skills && cp -r extensions/skills/* ~/.openhands/skills/
mkdir -p ~/.openhands/plugins && cp -r extensions/plugins/* ~/.openhands/plugins/
```
> 亦可用註冊表內 `add-skill` 技能從任意 GitHub repo 匯入單顆技能；專案層放 `<repo>/.agents/skills/`，使用者層放 `~/.agents/skills/`。

## 4-2. Extensions 註冊表 56 項（05–60，含官方說明濃縮；★=plugin 其餘=skill）

**05｜add-javadoc** — Java 類別/方法 JavaDoc 補全（large-codebase）
**06｜cobol-modernization★** — COBOL→Java 遷移全流程
**07｜migration-scoring★** — 遷移品質評分與報告
**08｜spark-version-upgrade** — Spark 2→3→4 升級
**09｜agent-canvas-environment** — Canvas 本地環境操作規範
**10｜agent-creator** — 檔案式子代理建立（/agent-creator）
**11｜agent-memory** — AGENTS.md 知識持久化（/remember）
**12｜agent-sdk-builder** — 以 SDK 自建 agent（/agent-builder）
**13｜azure-devops** — AzDO repo/PR/API 操作
**14｜bitbucket** + **15｜bitbucket-cloud** + **16｜bitbucket-data-center**** — Bitbucket 雙版本整合
**17｜canvas-extension-api** — Agent Canvas 應用開發
**18｜city-weather★** — Open-Meteo 天氣（免 key）
**19｜code-review** — 嚴格審查（/codereview、/codereview-roasted）
**20｜code-simplifier** — 三維度簡化（/simplify）
**21｜datadog** — 日誌/指標/APM 查詢
**22｜deno** — Deno 專案操作
**23｜discord** — Discord bot/webhook 整合
**24｜docker** — 容器內 Docker 操作
**25｜evidence-based-citations** — 事實主張附可查證來源
**26｜frontend-design** — 高品質前端介面產出
**27｜github** — GH repo/PR/issue 操作
**28｜github-actions** — CI workflow 開發與除錯
**29｜github-agents-md-maintainer** — 定時維護 AGENTS.md
**30｜github-delivery-watchdog** — 定時檢查並合併綠燈 PR
**31｜github-issue-to-pr** — 標籤觸發 issue 自動實作
**32｜github-issue-triage** — issue 優先級與驗收條件
**33｜github-pr-review** — 單次 API 送出結構化 PR 審查
**34｜github-pr-reviewer** — PR 開啟/更新自動審查
**35｜github-repo-monitor** — 定時輪詢 issue/PR 評論觸發
**36｜gitlab** + **37｜gitlab-issue-to-mr**** — GitLab 整合
**38｜incident-retrospective** — 事件回溯報告自動化
**39｜iterate** — PR 迭代至可合併（/iterate、/verify、/babysit）
**40｜jira-issue-to-pr** — Jira 標籤觸發實作
**41｜jupyter** — .ipynb 讀寫執行轉換
**42｜kubernetes** — KIND 本地集群測試
**43｜learn-from-code-review** — 從 PR 回饋蒸餾技能
**44｜linear** + **45｜linear-triage**** — Linear 整合與自動分診
**46｜news-digest** — RSS 定時摘要（/news-digest:setup）
**47｜notion** — Notion 文件/資料庫
**48｜npm** — 非互動環境 npm 安裝
**49｜onboarding★** — repo agent-readiness 評估 + AGENTS.md 生成
**50｜openhands★** — Cloud CLI + REST API + Automations 合一
**51｜openhands-api** — Cloud/本地 agent-server API
**52｜openhands-automation** — 排程自動化（/automation:create）
**53｜openhands-enterprise-troubleshooting** — 企業版自架除錯
**54｜openhands-sdk** — SDK 參考技能（/sdk）
**55｜pdflatex** — LaTeX→PDF 編譯
**56｜plain-english-content** — 平實英文寫作
**57｜pr-review★** — 自動 PR diff 審查 + 行內評論
**58｜prd** — 互動式 PRD 產生（/prd）
**59｜qa-changes★** — 實際執行程式碼驗證 PR 變更
**60｜release-notes★** — git 歷史產出 changelog（/release-notes）

> 註冊表另有（可直接以 04 方法全裝）：research-brief、security、skill-creator、slack-channel-monitor、slack-standup-digest、ssh、swift-linux、technical-writing、theme-factory、ticket-to-code-change、upstream-fork-sync、uv、vercel、vulnerability-remediation★。

---

# 五、紅隊 / Jailbreak 安全測試專區（僅限自己擁有的本地/私有端點）

這些是業界標準 LLM 紅隊框架，安裝即用，專門測「你自己的模型部署」：

```bash
# 1. garak（NVIDIA 出品，LLM 漏洞掃描器：越獄/promptinject/毒性/惡意程式生成探針）
pip install garak
python -m garak --model_type openai --generator_options '{"base_url":"http://你的端點/v1","api_key":"sk-..."}' --probes promptinject,dan,jailbreak,encoding

# 2. PyRIT（Microsoft 風險識別工具，多輪對抗编排）
pip install pyrit-ai

# 3. promptfoo（評測 + redteam 變體生成 + CI 整合）
npm i -g promptfoo
promptfoo redteam init

# 4. deepteam（Confident AI，紅隊測試框架）
pip install deepteam

# 5. Agentic Security（agent 漏洞掃描）
pip install agentic-security

# 6. LLM Guard（ProtectAI，防護側：prompt injection 偵測/輸出過濾，可掛進 OpenWebUI filter）
pip install llm-guard

# 7. PyPromptInject（提示注入基準資料集，評估韌性）
pip install pypromptinject
```

平台內建防護項：DSH 的 `dsh-defend`/`dsh-vet`/`dsh-poison-guard`；OpenWebUI 的 Detoxify Filter + LLM Guard filter；Hermes skill「prompt-injection-test」「garak-runner」；OpenHands `security`、`vulnerability-remediation` 技能。

---

# 六、手機程式開發專區（跨平台串聯）

```bash
# Termux（Android 本機開發環境）
pkg update && pkg upgrade -y && pkg install -y git clang python nodejs-lts openjdk-17 gradle android-tools

# Android 逆向/分析三件套（PC）
pip install apktool-jadx || true
# 或手動：jadx（GitHub 下載）、apktool、frida → pip install frida frida-tools

# Flutter / React Native 工具鏈
git clone https://github.com/flutter/flutter.git -b stable && export PATH="$PATH:$PWD/flutter/bin"
npm i -g eas-cli react-native-cli

# iOS（macOS）：Xcode Command Line Tools + fastlane + CocoaPods
xcode-select --install
gem install fastlane
gem install cocoapods
```

搭配掛載：DSH 的 `dsh-adb` + DSHBox（手機跑 agent 幫你寫手機程式）、Hermes WebUI（手機瀏覽器操作）、OpenWebUI PWA、`android-dev`/`flutter-dev`/`ios-dev` skills。

---

# 七、協作開發組合（多 agent 協同作業流）

1. **Hermes × DSH**：`dsh plugin --profile web add hermes-dsh-collab`（dispatch 模板 + 模型分層路由 + 品質閘門 + git 單寫者規則）
2. **DSH 多機**：`dsh-collaboration`（team_call/team_message/team_status）+ `dsh-team-rooms`（跨 session 訊息匯流排）
3. **OpenHands 全自動 issue→PR**：`github-issue-to-pr` + `github-pr-reviewer` + `iterate` + Resolver Action
4. **OpenWebUI 團隊入口**：Channels + OAuth/LDAP + Rate Limit Filter + Langfuse 觀測
5. **跨平台記憶互通**：`dsh-skill-mover`（14 平台技能搬遷）、`dsh-claude-move`（Claude Code/Codex/Hermes→DSH）、OpenHands `add-skill`、Hermes USER.md 觀測層

---

*資料截至 2026-09-24；DSH 為開發者預覽版，API 可能破壞性變更，安裝外掛前建議先跑 `dsh-vet`。*
# 三、OpenWebUI — 70 項

OpenWebUI 的可掛載面：**Tools（給模型新能力）/ Functions（改變 WebUI 本身：Pipe、Filter、Action、Event）/ Skills（SKILL.md，模型可 view_skill 載入）/ MCP 工具伺服器 / 內建工具類別開關**。安裝主體：

**A0｜三種主體安裝（擇一）**
```bash
# PyPI
pip install open-webui
open-webui serve
# Docker（依你的要求省略 port 映射，請自行加上）
docker run -d -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
# Kubernetes
helm repo add open-webui https://helm.openwebui.com
helm install open-webui open-webui/open-webui
```

## 3-1. 內建能力開關（12 項，Admin → Settings → General 或 docker -e）

01｜Web Search：`ENABLE_WEB_SEARCH=true`、`WEB_SEARCH_ENGINE`（searxng/brave/google_pse/tavily/exa/duckduckgo/morph）
02｜混合檢索：`ENABLE_RAG_HYBRID_SEARCH=true`（內建工具 query_knowledge_files 走 hybrid+rerank）
03｜圖片生成：`ENABLE_IMAGE_GENERATION=true` + `IMAGE_GENERATION_ENGINE`（openai/comfyui/gemini）
04｜圖片編輯：`ENABLE_IMAGE_EDIT=true`
05｜沙箱程式執行：`ENABLE_CODE_INTERPRETER=true`（內建 execute_code 工具）
06｜頻道：`ENABLE_CHANNELS=true`（Teams/Slack/Discord 式頻道）
07｜筆記：`ENABLE_NOTES=true`
08｜KB 檔案系統介面：`ENABLE_KB_EXEC=true`（kb_exec：ls/tree/grep/cat 等）
09｜OAuth/OIDC：Google/GitHub/Microsoft/Authentik/Keycloak 登入開關
10｜LDAP 企業登入 + SMTP 郵件
11｜記憶體系統：Memory（個人化記憶）於 Admin 啟用，內建 add/search/update/delete 工具
12｜任務/行事曆/自動化內建工具：Task Management、Calendar、Automations（create/toggle/delete）

## 3-2. 社群函數庫 Tools & Functions（25 項，一鍵：Workspace → Tools / Admin → Functions → + → 從社群匯入，搜尋以下名稱）

13｜SearXNG Web Search（tool）— 免費自架搜尋
14｜Brave Web Search（tool）— 需 Brave API key
15｜Google Programmable Search（tool）
16｜Tavily Web Search（tool）— 附帶 extract
17｜Exa Web Search（tool）— 神經搜尋
18｜DuckDuckGo Search（tool）— 免 key
19｜Website RAG（tool）— 整站抓取而量產 embedding
20｜YouTube RAG（tool）— `docker exec open-webui pip install youtube-transcript-api`
21｜Memory / 長期記憶（function, filter）
22｜OpenAI Image Generation（pipe/manifold）
23｜ComfyUI Image Generation（pipe）— 接 ComfyUI 工作流
24｜Gemini Image Generation（pipe）
25｜DALL-E Manifold（pipe）— 多模型管理
26｜Function Calling（內建開關 + 社群增強版）
27｜Code Interpreter（內建 + 社群 Pyodide 版）
28｜Prompt Generation（function）— 自動潤飾 prompt
29｜Title Generation（function）— 對話命名
30｜LlamaIndex RAG（pipeline/legacy）：`pip install llama-index`
31｜Mem0 Memory（function）：`pip install mem0ai`
32｜Langfuse Filter（function，LLM 可觀測性）：`pip install langfuse`
33｜OpenTelemetry Filter：`pip install opentelemetry-sdk opentelemetry-exporter-otlp`
34｜Detoxify Filter（毒性內容過濾，紅隊必備）：`pip install detoxify`
35｜Rate Limit Filter（限速防刷）
36｜LibreTranslate Filter（即時翻譯）：接本地 libretranslate
37｜Inject Stats Filter（回應附帶 token 統計）

## 3-3. MCP 工具伺服器（12 項，Admin → Settings → External Tools 加入 MCP server）

```bash
# 常用 MCP server 啟動指令（於 OpenWebUI 的 MCP 設定中填寫）
38｜filesystem：npx -y @modelcontextprotocol/server-filesystem /允許目錄
39｜github：npx -y @modelcontextprotocol/server-github（需 GITHUB_TOKEN）
40｜gitlab：npx -y @modelcontextprotocol/server-gitlab
41｜postgres：npx -y @modelcontextprotocol/server-postgres 連線字串
42｜sqlite：npx -y @modelcontextprotocol/server-sqlite 資料庫路徑
43｜fetch：uvx mcp-server-fetch
44｜memory：npx -y @modelcontextprotocol/server-memory
45｜sequential-thinking：npx -y @modelcontextprotocol/server-sequential-thinking
46｜brave-search：npx -y @modelcontextprotocol/server-brave-search
47｜playwright：npx -y @playwright/mcp@latest（瀏覽器自動化）
48｜puppeteer：npx -y @modelcontextprotocol/server-puppeteer
49｜slack：npx -y @modelcontextprotocol/server-slack
```

## 3-4. Skills（10 顆，複製貼到 Workspace → Skills → 新增 → 貼上 frontmatter 內容）

50｜android-dev
```
---
name: android-dev
description: Android 開發輔助：Gradle 除錯、logcat 分析、Compose 審查。當使用者處理 Android 專案時使用。
---
1. 先判斷問題類型：建置/執行期/UI
2. 建置錯誤→執行 ./gradlew build 收錯誤堆疊
3. 執行期→adb logcat -b crash 定位
4. Compose 問題→檢查 recomposition 與狀態提升
5. 輸出：根因 + 最小修復 patch
```
51｜ios-dev（SwiftUI/SwiftData/Xcode 建置排查）
52｜flutter-dev（pub deps、EAS、OTA 更新流程）
53｜react-native-dev（Metro、原生模組、OTA）
54｜redteam-local-llm（對自有端點之 garak/promptfoo 授權測試流程）
55｜secure-code-review（OWASP 導向審查流程）
56｜api-design（REST/GraphQL 設計檢查清單）
57｜tdd-loop（紅綠重構紀律）
58｜release-checklist（語義化版本、changelog、artifact 校驗）
59｜ci-debug（CI 失敗本機復現流程）
60｜db-migration（零停機遷移擴張收縮法）

> 使用方式：Workspace → Models → 編輯模型 → Skills 勾選 → 模型獲得 view_skill 工具，按需載入全文，不佔 context。

## 3-5. 容器內補強與周邊（10 項）

61｜工具依賴批次安裝：
```bash
docker exec open-webui pip install youtube-transcript-api llama-index mem0ai langfuse detoxify duckduckgo-search tavily-python exa-py
```
62｜本機模型：安裝 Ollama 後於 Connections 加入（GPU 可用 open-webui 官方 cuda 映像檔）
63｜本地 TTS/STT：Admin → Audio 設定 OpenAI-compatible TTS（如 piper/localai）
64｜RAG embedding：Admin → Documents 設定本地 sentence-transformers 或 Ollama embedding
65｜向量庫外接：Chroma/Qdrant/Milvus/Pgvector/Weaviate 設定於 Admin → Documents
66｜Reranker：啟用 RAG rerank（FlashRank/Jina/Cohere）
67｜LiteLLM 代理：以 litellm 串接 100+ provider 後於 Connections 指向
68｜行動 PWA：手機瀏覽器「加到主畫面」即 App；或用社群 open-webui mobile app 專案
69｜備份：`docker cp open-webui:/app/backend/data ./backup`
70｜外網安全：啟用登入驗證 + OAuth + Rate Limit Filter（見 35）+ HTTPS 反向代理


---

# 四、OpenHands（原 OpenDevin，All Hands AI）— 60 項

OpenHands 的可掛載面：**Skills（SKILL.md，~/.openhands/skills 或 ~/.agents/skills 自動載入）/ Plugins（hooks+scripts）/ Extensions 公開註冊表（73 個：63 skills + 10 plugins）/ MCP 工具 / Automations 自動化**。SDK/CLI 支援 LLM via LiteLLM（100+ provider）。

## 4-1. 核心安裝（4 項）

**01｜pip 安裝（CLI + SDK）**
```bash
pip install openhands-ai
openhands
```
**02｜Docker 主體（依要求省略 port 映射）**
```bash
docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock -v $HOME/.openhands-state:/.openhands-state --name openhands all-hands-ai/openhands
```
**03｜GitHub Resolver（issue→PR 自動化 Action）**** — repo 加 `.github/workflows/openhands-resolver.yml`（官方範例於 OpenHands/OpenHands repo）
**04｜Extensions 註冊表全量 Skills 載入**
```bash
git clone --depth 1 https://github.com/openhands/extensions.git
mkdir -p ~/.openhands/skills && cp -r extensions/skills/* ~/.openhands/skills/
mkdir -p ~/.openhands/plugins && cp -r extensions/plugins/* ~/.openhands/plugins/
```
> 亦可用註冊表內 `add-skill` 技能從任意 GitHub repo 匯入單顆技能；專案層放 `<repo>/.agents/skills/`，使用者層放 `~/.agents/skills/`。

## 4-2. Extensions 註冊表 56 項（05–60，含官方說明濃縮；★=plugin 其餘=skill）

**05｜add-javadoc** — Java 類別/方法 JavaDoc 補全（large-codebase）
**06｜cobol-modernization★** — COBOL→Java 遷移全流程
**07｜migration-scoring★** — 遷移品質評分與報告
**08｜spark-version-upgrade** — Spark 2→3→4 升級
**09｜agent-canvas-environment** — Canvas 本地環境操作規範
**10｜agent-creator** — 檔案式子代理建立（/agent-creator）
**11｜agent-memory** — AGENTS.md 知識持久化（/remember）
**12｜agent-sdk-builder** — 以 SDK 自建 agent（/agent-builder）
**13｜azure-devops** — AzDO repo/PR/API 操作
**14｜bitbucket** + **15｜bitbucket-cloud** + **16｜bitbucket-data-center**** — Bitbucket 雙版本整合
**17｜canvas-extension-api** — Agent Canvas 應用開發
**18｜city-weather★** — Open-Meteo 天氣（免 key）
**19｜code-review** — 嚴格審查（/codereview、/codereview-roasted）
**20｜code-simplifier** — 三維度簡化（/simplify）
**21｜datadog** — 日誌/指標/APM 查詢
**22｜deno** — Deno 專案操作
**23｜discord** — Discord bot/webhook 整合
**24｜docker** — 容器內 Docker 操作
**25｜evidence-based-citations** — 事實主張附可查證來源
**26｜frontend-design** — 高品質前端介面產出
**27｜github** — GH repo/PR/issue 操作
**28｜github-actions** — CI workflow 開發與除錯
**29｜github-agents-md-maintainer** — 定時維護 AGENTS.md
**30｜github-delivery-watchdog** — 定時檢查並合併綠燈 PR
**31｜github-issue-to-pr** — 標籤觸發 issue 自動實作
**32｜github-issue-triage** — issue 優先級與驗收條件
**33｜github-pr-review** — 單次 API 送出結構化 PR 審查
**34｜github-pr-reviewer** — PR 開啟/更新自動審查
**35｜github-repo-monitor** — 定時輪詢 issue/PR 評論觸發
**36｜gitlab** + **37｜gitlab-issue-to-mr**** — GitLab 整合
**38｜incident-retrospective** — 事件回溯報告自動化
**39｜iterate** — PR 迭代至可合併（/iterate、/verify、/babysit）
**40｜jira-issue-to-pr** — Jira 標籤觸發實作
**41｜jupyter** — .ipynb 讀寫執行轉換
**42｜kubernetes** — KIND 本地集群測試
**43｜learn-from-code-review** — 從 PR 回饋蒸餾技能
**44｜linear** + **45｜linear-triage**** — Linear 整合與自動分診
**46｜news-digest** — RSS 定時摘要（/news-digest:setup）
**47｜notion** — Notion 文件/資料庫
**48｜npm** — 非互動環境 npm 安裝
**49｜onboarding★** — repo agent-readiness 評估 + AGENTS.md 生成
**50｜openhands★** — Cloud CLI + REST API + Automations 合一
**51｜openhands-api** — Cloud/本地 agent-server API
**52｜openhands-automation** — 排程自動化（/automation:create）
**53｜openhands-enterprise-troubleshooting** — 企業版自架除錯
**54｜openhands-sdk** — SDK 參考技能（/sdk）
**55｜pdflatex** — LaTeX→PDF 編譯
**56｜plain-english-content** — 平實英文寫作
**57｜pr-review★** — 自動 PR diff 審查 + 行內評論
**58｜prd** — 互動式 PRD 產生（/prd）
**59｜qa-changes★** — 實際執行程式碼驗證 PR 變更
**60｜release-notes★** — git 歷史產出 changelog（/release-notes）

> 註冊表另有（可直接以 04 方法全裝）：research-brief、security、skill-creator、slack-channel-monitor、slack-standup-digest、ssh、swift-linux、technical-writing、theme-factory、ticket-to-code-change、upstream-fork-sync、uv、vercel、vulnerability-remediation★。

---

# 五、紅隊 / Jailbreak 安全測試專區（僅限自己擁有的本地/私有端點）

這些是業界標準 LLM 紅隊框架，安裝即用，專門測「你自己的模型部署」：

```bash
# 1. garak（NVIDIA 出品，LLM 漏洞掃描器：越獄/promptinject/毒性/惡意程式生成探針）
pip install garak
python -m garak --model_type openai --generator_options '{"base_url":"http://你的端點/v1","api_key":"sk-..."}' --probes promptinject,dan,jailbreak,encoding

# 2. PyRIT（Microsoft 風險識別工具，多輪對抗编排）
pip install pyrit-ai

# 3. promptfoo（評測 + redteam 變體生成 + CI 整合）
npm i -g promptfoo
promptfoo redteam init

# 4. deepteam（Confident AI，紅隊測試框架）
pip install deepteam

# 5. Agentic Security（agent 漏洞掃描）
pip install agentic-security

# 6. LLM Guard（ProtectAI，防護側：prompt injection 偵測/輸出過濾，可掛進 OpenWebUI filter）
pip install llm-guard

# 7. PyPromptInject（提示注入基準資料集，評估韌性）
pip install pypromptinject
```

平台內建防護項：DSH 的 `dsh-defend`/`dsh-vet`/`dsh-poison-guard`；OpenWebUI 的 Detoxify Filter + LLM Guard filter；Hermes skill「prompt-injection-test」「garak-runner」；OpenHands `security`、`vulnerability-remediation` 技能。

---

# 六、手機程式開發專區（跨平台串聯）

```bash
# Termux（Android 本機開發環境）
pkg update && pkg upgrade -y && pkg install -y git clang python nodejs-lts openjdk-17 gradle android-tools

# Android 逆向/分析三件套（PC）
pip install apktool-jadx || true
# 或手動：jadx（GitHub 下載）、apktool、frida → pip install frida frida-tools

# Flutter / React Native 工具鏈
git clone https://github.com/flutter/flutter.git -b stable && export PATH="$PATH:$PWD/flutter/bin"
npm i -g eas-cli react-native-cli

# iOS（macOS）：Xcode Command Line Tools + fastlane + CocoaPods
xcode-select --install
gem install fastlane
gem install cocoapods
```

搭配掛載：DSH 的 `dsh-adb` + DSHBox（手機跑 agent 幫你寫手機程式）、Hermes WebUI（手機瀏覽器操作）、OpenWebUI PWA、`android-dev`/`flutter-dev`/`ios-dev` skills。

---

# 七、協作開發組合（多 agent 協同作業流）

1. **Hermes × DSH**：`dsh plugin --profile web add hermes-dsh-collab`（dispatch 模板 + 模型分層路由 + 品質閘門 + git 單寫者規則）
2. **DSH 多機**：`dsh-collaboration`（team_call/team_message/team_status）+ `dsh-team-rooms`（跨 session 訊息匯流排）
3. **OpenHands 全自動 issue→PR**：`github-issue-to-pr` + `github-pr-reviewer` + `iterate` + Resolver Action
4. **OpenWebUI 團隊入口**：Channels + OAuth/LDAP + Rate Limit Filter + Langfuse 觀測
5. **跨平台記憶互通**：`dsh-skill-mover`（14 平台技能搬遷）、`dsh-claude-move`（Claude Code/Codex/Hermes→DSH）、OpenHands `add-skill`、Hermes USER.md 觀測層

---

*資料截至 2026-09-24；DSH 為開發者預覽版，API 可能破壞性變更，安裝外掛前建議先跑 `dsh-vet`。*
git clone https://github.com/flutter/flutter.git -b stable && export PATH="$PATH:$PWD/flutter/bin"
npm i -g eas-cli react-native-cli

# iOS（macOS）：Xcode Command Line Tools + fastlane + CocoaPods
xcode-select --install
gem install fastlane
gem install cocoapods
```

搭配掛載：DSH 的 `dsh-adb` + DSHBox（手機跑 agent 幫你寫手機程式）、Hermes WebUI（手機瀏覽器操作）、OpenWebUI PWA、`android-dev`/`flutter-dev`/`ios-dev` skills。

---

# 七、協作開發組合（多 agent 協同作業流）

1. **Hermes × DSH**：`dsh plugin --profile web add hermes-dsh-collab`（dispatch 模板 + 模型分層路由 + 品質閘門 + git 單寫者規則）
2. **DSH 多機**：`dsh-collaboration`（team_call/team_message/team_status）+ `dsh-team-rooms`（跨 session 訊息匯流排）
3. **OpenHands 全自動 issue→PR**：`github-issue-to-pr` + `github-pr-reviewer` + `iterate` + Resolver Action
4. **OpenWebUI 團隊入口**：Channels + OAuth/LDAP + Rate Limit Filter + Langfuse 觀測
5. **跨平台記憶互通**：`dsh-skill-mover`（14 平台技能搬遷）、`dsh-claude-move`（Claude Code/Codex/Hermes→DSH）、OpenHands `add-skill`、Hermes USER.md 觀測層

---

*資料截至 2026-09-24；DSH 為開發者預覽版，API 可能破壞性變更，安裝外掛前建議先跑 `dsh-vet`。*
