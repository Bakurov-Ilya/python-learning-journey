# Пошаговый план создания OpenClaw агента на VPS с доступом через Telegram

## Предварительные требования и предупреждения
- **VPS**: Рекомендую Ubuntu 22.04 LTS с минимум 4GB RAM, 2 CPU (Node.js >=22). Для модели qwen/qwen2.5-72b-instruct (или аналогичной 122B, точное имя проверьте на провайдере) **локальный запуск невозможен** без мощного GPU (A100/H100 80GB+ VRAM). Используйте **API-провайдера** (Together.ai, OpenRouter.ai, HuggingFace Inference Endpoints) с OpenAI-compatible API. Стоимость ~$1-5/час inference или $0.5-2/млн токенов.
- **Доступ**: SSH к VPS. Telegram Bot Token от [@BotFather](https://t.me/botfather).
- **Безопасность**: Firewall (ufw), non-root user, Tailscale/Cloudflare Tunnel/SSH tunnel для Gateway (порт 18789). Никогда не открывайте порты публично без auth.
- **Зависимости**: Node.js 22+, npm/pnpm/bun, git.

## Пошаговый план установки (выполняйте по SSH как non-root user)

### Шаг 1: Подготовка VPS
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install curl wget git ufw nodejs npm -y  # Node из nodesource ниже
ufw allow OpenSSH && ufw allow 22/tcp && ufw --force enable
adduser openclaw-user  # Создайте dedicated user
usermod -aG sudo openclaw-user
su - openclaw-user
```

### Шаг 2: Установка Node.js 22+
```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
node --version  # >=22.x
npm install -g pnpm  # pnpm предпочтительнее
```

### Шаг 3: Установка OpenClaw
```bash
pnpm add -g openclaw@latest
openclaw doctor  # Диагностика окружения
```

### Шаг 4: Onboarding Wizard
```bash
openclaw onboard --install-daemon
```
- Wizard настроит Gateway, workspace, models, channels.
- **Модели**: Настройте Qwen через OpenAI-compatible API:
  В `~/.openclaw/openclaw.json` или wizard:
  ```json
  {
    "agent": {
      "model": "qwen/qwen2.5-72b-instruct",  // Или qwen/qwen3.5-122b-a10b если доступно; проверьте на провайдере
      "provider": "openai",
      "baseUrl": "https://api.together.xyz/v1",  // Together.ai пример
      "apiKey": "YOUR_TOGETHER_API_KEY"
    },
    "models": [
      {
        "name": "qwen-main",
        "provider": "openai",
        "model": "qwen/qwen2.5-72b-instruct",
        "baseUrl": "https://api.together.xyz/v1",
        "apiKey": "YOUR_API_KEY"
      }
    ]
  }
  ```
- Рекомендация: Anthropic Claude как fallback для безопасности.

### Шаг 5: Настройка Telegram Bot
1. [@BotFather](https://t.me/botfather) → /newbot → Username (e.g. myopenclaw_bot) → Получите **BOT_TOKEN**.
2. Ваш Telegram ID: [@userinfobot](https://t.me/userinfobot).
3. В config/wizard:
   ```json
   {
     "channels": {
       "telegram": {
         "botToken": "1234567890:ABCdefGhIJKlmNoPQRstUvWxYz",
         "allowFrom": ["YOUR_TELEGRAM_USER_ID"],  // Только вы!
         "dmPolicy": "pairing"  // Безопасность: pairing code для новых
       }
     }
   }
   ```
4. Перезапустите: `openclaw gateway restart`.

### Шаг 6: Запуск и автозапуск
- Wizard создаст systemd user service.
- Проверьте: `systemctl --user status openclaw`
- Логи: `journalctl --user -u openclaw -f`
- Тест CLI: `openclaw agent --message "Тест Qwen агента"`

### Шаг 7: Доступ к Dashboard (опционально, безопасно)
- **Tailscale** (рекомендую): Установите Tailscale на VPS и локально, `tailscale serve 18789`.
- **SSH Tunnel**: `ssh -L 18789:localhost:18789 user@vps` → http://localhost:18789
- Никогда не открывайте 18789 публично!

### Шаг 8: Тестирование
- Напишите боту в Telegram: "Привет!".
- Агент ответит через Qwen.
- CLI: `openclaw message send --channel telegram --to YOUR_ID --message "Тест"`

### Шаг 9: Мониторинг, обновления, безопасность
- `openclaw doctor` - ежедневно.
- Обновление: `openclaw update`.
- Логи/usage: Dashboard.
- Sandbox: В config `"agents.defaults.sandbox.mode": "non-main"` для групп.
- Backup: `~/.openclaw/` (config, creds).

## Возможные проблемы
- **Модель не работает**: Проверьте API key, baseUrl, модель имя на [Together.ai models](https://together.ai/models).
- **Telegram не отвечает**: Проверьте botToken, allowFrom, firewall.
- **Node версия**: Только >=22.
- **Ресурсы**: Мониторьте RAM/CPU; для heavy use - VPS 8GB+.

## Стоимость примера
- VPS (DigitalOcean 4GB): ~$24/мес.
- Qwen API: ~$1/млн input + $3/млн output токенов.

План готов к выполнению! Если нужны изменения - отредактируйте `openclaw-vps-plan.md`.

**Уточнения (ответьте для доработки):**
1. VPS провайдер (DigitalOcean, Vultr)? Конфиг (RAM/CPU)?
2. API для Qwen (Together.ai key? OpenRouter?)?
3. Готовы Bot Token / User ID?
