### line_provider и bet_maker

Данный проект демонстрирует архитектуру взаимодействия двух микросервисов (**line_provider** и  **bet_maker** ) через RabbitMQ, а также хранение ставок в PostgreSQL.

```
docker-compose up --build
```

После чего:

* line_provider будет доступен на порту **8001**.
* bet_maker будет доступен на порту **8002**.

* RabbitMQ (с веб-интерфейсом) — на порту **15672**.
* PostgreSQL — на порту **5432**.

Далее можно отправлять тестовые запросы через **curl** или Postman, проверять логи сервисов и корректную обработку ставок.

```
bsw-test-line-provider
├─ .DS_Store
├─ .git
│  ├─ COMMIT_EDITMSG
│  ├─ FETCH_HEAD
│  ├─ HEAD
│  ├─ ORIG_HEAD
│  ├─ config
│  ├─ description
│  ├─ hooks
│  │  ├─ applypatch-msg.sample
│  │  ├─ commit-msg.sample
│  │  ├─ fsmonitor-watchman.sample
│  │  ├─ post-update.sample
│  │  ├─ pre-applypatch.sample
│  │  ├─ pre-commit.sample
│  │  ├─ pre-merge-commit.sample
│  │  ├─ pre-push.sample
│  │  ├─ pre-rebase.sample
│  │  ├─ pre-receive.sample
│  │  ├─ prepare-commit-msg.sample
│  │  ├─ push-to-checkout.sample
│  │  └─ update.sample
│  ├─ index
│  ├─ info
│  │  └─ exclude
│  ├─ logs
│  │  ├─ HEAD
│  │  └─ refs
│  │     ├─ heads
│  │     │  └─ main
│  │     └─ remotes
│  │        └─ origin
│  │           └─ main
│  ├─ objects
│  │  ├─ 02
│  │  │  └─ 2c0009c94000e5962257c8f5fbe2bc8cd48068
│  │  ├─ 06
│  │  │  └─ 3b13f96f7eb65ea9ea3b27ce24ca7ce04420de
│  │  ├─ 08
│  │  │  └─ 90314ed6b59228fccc49f4200a78966af4209f
│  │  ├─ 0a
│  │  │  └─ 6809b2ef0f66ea23bdef885f6a9e102c36a12c
│  │  ├─ 0b
│  │  │  └─ ec59a8f889935d94031adedd6357ccbf1224c2
│  │  ├─ 10
│  │  │  ├─ 815c2c2bae9320e0146876d14fada34430aebe
│  │  │  └─ cd2f315b84e0a9a1a1234c2ae1f8a3099a589e
│  │  ├─ 13
│  │  │  └─ 612ddb725a6f4019e173ae45da892705636b1f
│  │  ├─ 15
│  │  │  └─ 711cc05495ade567cd28696bb91a967ef315e0
│  │  ├─ 1b
│  │  │  └─ 33d99bd7e0371a74ffa9795dcb02720f129b4a
│  │  ├─ 1c
│  │  │  └─ d3cfacb2d18072d3cf6c93dfb4d0555fe40578
│  │  ├─ 25
│  │  │  └─ a7ac9818ae07a2e4eb27310faa7a434b3c3538
│  │  ├─ 3d
│  │  │  └─ c0057a91b8bfc4a635457af22f18a885af8b3b
│  │  ├─ 45
│  │  │  └─ 98b4c8106722159641656afdfd738fcd5b7eaa
│  │  ├─ 4b
│  │  │  └─ 825dc642cb6eb9a060e54bf8d69288fbee4904
│  │  ├─ 54
│  │  │  └─ fe924743d8b9e424ef201dcabcdd6b42241745
│  │  ├─ 58
│  │  │  └─ 6be83aa698e529425bf70cf53d3c3cc1dc264b
│  │  ├─ 59
│  │  │  └─ 29fbac94f6570de05b334079e8f51692d7ef3d
│  │  ├─ 5f
│  │  │  └─ 6c289f97e9e6b244e4b36e4ed1dfca4f972353
│  │  ├─ 65
│  │  │  └─ dafd31ca85d98298f7dc6e6b9e9077b558b733
│  │  ├─ 72
│  │  │  └─ 29ef75fef19bfa3d8aa256ecf27b3a7431e480
│  │  ├─ 76
│  │  │  └─ 7ea5060d9d94997c5028f73502a1013a82d8bc
│  │  ├─ 7f
│  │  │  └─ 053b45a190479ceec3cfa5a59e4d8dbcc8939b
│  │  ├─ 88
│  │  │  └─ 315dae8ef33b41e3f2f2f1aff1c160ca99860f
│  │  ├─ 8c
│  │  │  └─ 60b26a30030efe14d7850bca73de78a91b673a
│  │  ├─ 92
│  │  │  └─ 526863a7e4aadccd8358d9b29e12bf40735edc
│  │  ├─ 95
│  │  │  └─ 70174d7effd377d20556a16b345caf5e854c04
│  │  ├─ 98
│  │  │  └─ 029cc3a797197671e6533ae68ba806968bfd70
│  │  ├─ 99
│  │  │  └─ ddf2695701e725c77f7dc11cb96a5b1107effa
│  │  ├─ 9f
│  │  │  └─ 306b1d270601bb409fd3830265877c6863b0d7
│  │  ├─ ac
│  │  │  └─ 76b50eb2fd8887e563da8ead53dfb82d2a58ed
│  │  ├─ b8
│  │  │  └─ 00a77ef8a875cac84820da5736e71eaa43f59c
│  │  ├─ b9
│  │  │  └─ 4a0a7ac3f0faa66c19986c18ded0e116f4cda6
│  │  ├─ bd
│  │  │  └─ 30ce639a1362039a666985f5f09ef30d680f0a
│  │  ├─ c6
│  │  │  └─ 47a2fd0ff622889caa44fe3e97fa33cb988ec9
│  │  ├─ d1
│  │  │  └─ 14e0d7c7a96d9efdf9537ad28ad48ce73d9918
│  │  ├─ d7
│  │  │  └─ a6a198ccbe0c3cbbb91327b991cb67649037e9
│  │  ├─ e7
│  │  │  └─ 67cabb09740d9053761c61dc7f8fa96d78a98e
│  │  ├─ f0
│  │  │  └─ 5c12f656dad920304671f9af8c11c9e7d94e15
│  │  ├─ f5
│  │  │  └─ 791d64f47abeec876ddaa0be427a63bead899f
│  │  ├─ f7
│  │  │  └─ 79bdeab95e8138dc4ce7c574bf3ea754708d8f
│  │  ├─ fa
│  │  │  └─ 298b359dc959614fffa4aeb15cc9c389eb4a66
│  │  ├─ fc
│  │  │  └─ ce691942a129a0e4dbd5e4e1470469bc435635
│  │  ├─ info
│  │  └─ pack
│  └─ refs
│     ├─ heads
│     │  └─ main
│     ├─ remotes
│     │  └─ origin
│     │     └─ main
│     └─ tags
├─ .gitignore
├─ README.md
├─ bet_maker
│  ├─ Dockerfile
│  ├─ db.py
│  ├─ entrypoint.sh
│  ├─ main.py
│  ├─ models.py
│  ├─ requirements.txt
│  ├─ schemas.py
│  └─ tests
│     └─ test_bet_maker.py
├─ docker-compose.yml
├─ line_provider
│  ├─ Dockerfile
│  ├─ entrypoint.sh
│  ├─ main.py
│  ├─ requirements.txt
│  ├─ schemas.py
│  └─ tests
│     ├─ __init__.py
│     └─ test_line_provider.py
└─ pytest.ini

```
```
bsw-test-line-provider
├─ .DS_Store
├─ .git
│  ├─ COMMIT_EDITMSG
│  ├─ FETCH_HEAD
│  ├─ HEAD
│  ├─ ORIG_HEAD
│  ├─ config
│  ├─ description
│  ├─ hooks
│  │  ├─ applypatch-msg.sample
│  │  ├─ commit-msg.sample
│  │  ├─ fsmonitor-watchman.sample
│  │  ├─ post-update.sample
│  │  ├─ pre-applypatch.sample
│  │  ├─ pre-commit.sample
│  │  ├─ pre-merge-commit.sample
│  │  ├─ pre-push.sample
│  │  ├─ pre-rebase.sample
│  │  ├─ pre-receive.sample
│  │  ├─ prepare-commit-msg.sample
│  │  ├─ push-to-checkout.sample
│  │  └─ update.sample
│  ├─ index
│  ├─ info
│  │  └─ exclude
│  ├─ logs
│  │  ├─ HEAD
│  │  └─ refs
│  │     ├─ heads
│  │     │  └─ main
│  │     └─ remotes
│  │        └─ origin
│  │           └─ main
│  ├─ objects
│  │  ├─ 02
│  │  │  └─ 2c0009c94000e5962257c8f5fbe2bc8cd48068
│  │  ├─ 06
│  │  │  └─ 3b13f96f7eb65ea9ea3b27ce24ca7ce04420de
│  │  ├─ 08
│  │  │  └─ 90314ed6b59228fccc49f4200a78966af4209f
│  │  ├─ 0a
│  │  │  └─ 6809b2ef0f66ea23bdef885f6a9e102c36a12c
│  │  ├─ 0b
│  │  │  └─ ec59a8f889935d94031adedd6357ccbf1224c2
│  │  ├─ 10
│  │  │  ├─ 815c2c2bae9320e0146876d14fada34430aebe
│  │  │  └─ cd2f315b84e0a9a1a1234c2ae1f8a3099a589e
│  │  ├─ 13
│  │  │  └─ 612ddb725a6f4019e173ae45da892705636b1f
│  │  ├─ 15
│  │  │  └─ 711cc05495ade567cd28696bb91a967ef315e0
│  │  ├─ 1b
│  │  │  └─ 33d99bd7e0371a74ffa9795dcb02720f129b4a
│  │  ├─ 1c
│  │  │  └─ d3cfacb2d18072d3cf6c93dfb4d0555fe40578
│  │  ├─ 25
│  │  │  └─ a7ac9818ae07a2e4eb27310faa7a434b3c3538
│  │  ├─ 3d
│  │  │  └─ c0057a91b8bfc4a635457af22f18a885af8b3b
│  │  ├─ 45
│  │  │  └─ 98b4c8106722159641656afdfd738fcd5b7eaa
│  │  ├─ 4b
│  │  │  └─ 825dc642cb6eb9a060e54bf8d69288fbee4904
│  │  ├─ 54
│  │  │  └─ fe924743d8b9e424ef201dcabcdd6b42241745
│  │  ├─ 58
│  │  │  └─ 6be83aa698e529425bf70cf53d3c3cc1dc264b
│  │  ├─ 59
│  │  │  └─ 29fbac94f6570de05b334079e8f51692d7ef3d
│  │  ├─ 5f
│  │  │  └─ 6c289f97e9e6b244e4b36e4ed1dfca4f972353
│  │  ├─ 65
│  │  │  └─ dafd31ca85d98298f7dc6e6b9e9077b558b733
│  │  ├─ 72
│  │  │  └─ 29ef75fef19bfa3d8aa256ecf27b3a7431e480
│  │  ├─ 76
│  │  │  └─ 7ea5060d9d94997c5028f73502a1013a82d8bc
│  │  ├─ 7f
│  │  │  └─ 053b45a190479ceec3cfa5a59e4d8dbcc8939b
│  │  ├─ 88
│  │  │  └─ 315dae8ef33b41e3f2f2f1aff1c160ca99860f
│  │  ├─ 8c
│  │  │  └─ 60b26a30030efe14d7850bca73de78a91b673a
│  │  ├─ 92
│  │  │  └─ 526863a7e4aadccd8358d9b29e12bf40735edc
│  │  ├─ 95
│  │  │  └─ 70174d7effd377d20556a16b345caf5e854c04
│  │  ├─ 98
│  │  │  └─ 029cc3a797197671e6533ae68ba806968bfd70
│  │  ├─ 99
│  │  │  └─ ddf2695701e725c77f7dc11cb96a5b1107effa
│  │  ├─ 9f
│  │  │  └─ 306b1d270601bb409fd3830265877c6863b0d7
│  │  ├─ ac
│  │  │  └─ 76b50eb2fd8887e563da8ead53dfb82d2a58ed
│  │  ├─ b8
│  │  │  └─ 00a77ef8a875cac84820da5736e71eaa43f59c
│  │  ├─ b9
│  │  │  └─ 4a0a7ac3f0faa66c19986c18ded0e116f4cda6
│  │  ├─ bd
│  │  │  └─ 30ce639a1362039a666985f5f09ef30d680f0a
│  │  ├─ c6
│  │  │  └─ 47a2fd0ff622889caa44fe3e97fa33cb988ec9
│  │  ├─ d1
│  │  │  └─ 14e0d7c7a96d9efdf9537ad28ad48ce73d9918
│  │  ├─ d7
│  │  │  └─ a6a198ccbe0c3cbbb91327b991cb67649037e9
│  │  ├─ e7
│  │  │  └─ 67cabb09740d9053761c61dc7f8fa96d78a98e
│  │  ├─ f0
│  │  │  └─ 5c12f656dad920304671f9af8c11c9e7d94e15
│  │  ├─ f5
│  │  │  └─ 791d64f47abeec876ddaa0be427a63bead899f
│  │  ├─ f7
│  │  │  └─ 79bdeab95e8138dc4ce7c574bf3ea754708d8f
│  │  ├─ fa
│  │  │  └─ 298b359dc959614fffa4aeb15cc9c389eb4a66
│  │  ├─ fc
│  │  │  └─ ce691942a129a0e4dbd5e4e1470469bc435635
│  │  ├─ info
│  │  └─ pack
│  └─ refs
│     ├─ heads
│     │  └─ main
│     ├─ remotes
│     │  └─ origin
│     │     └─ main
│     └─ tags
├─ .gitignore
├─ README.md
├─ bet_maker
│  ├─ Dockerfile
│  ├─ __init__.py
│  ├─ db.py
│  ├─ entrypoint.sh
│  ├─ main.py
│  ├─ models.py
│  ├─ requirements.txt
│  ├─ schemas.py
│  └─ tests
│     └─ test_bet_maker.py
├─ docker-compose.yml
├─ line_provider
│  ├─ Dockerfile
│  ├─ __init__.py
│  ├─ entrypoint.sh
│  ├─ main.py
│  ├─ requirements.txt
│  ├─ schemas.py
│  └─ tests
│     ├─ __init__.py
│     └─ test_line_provider.py
└─ pytest.ini

```