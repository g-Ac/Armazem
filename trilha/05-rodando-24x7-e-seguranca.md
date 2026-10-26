# Módulo 05 — Rodando 24/7 no Servidor e Segurança na Prática

> **Tempo estimado:** 35 minutos
> **Meta prática:** tirar o sistema do seu notebook (que desliga quando fecha a tampa) e colocá-lo rodando 24/7 num Linux (Raspberry Pi, PC antigo em casa ou VPS barata), sem vazar segredos nem deixar portas abertas para curiosos.

---

## 1. Onde rodar seus sistemas 24/7 gastando quase nada?

Você tem 3 ótimas opções para começar:
1. **Um Raspberry Pi ou notebook/PC antigo com Ubuntu Server em casa**: custo mensal quase zero de energia, excelente para bots, coletores, automações e homelab.
2. **Uma VPS Linux de entrada** (Hetzner, DigitalOcean, Oracle Free Tier, etc.): ideal quando um site precisa ficar acessível publicamente com domínio próprio.
3. **Arquitetura Híbrida (Pi + Servidor em rede privada)**: uma máquina leve ligada 24/7 orquestrando alertas no Telegram + uma máquina mais forte para processar IA local, conectadas por **Tailscale** sem abrir nenhuma porta no roteador de casa (veja o mapa real em [`g-Ac/homelab`](https://github.com/g-Ac/homelab)).

---

## 2. `systemd`: o vigia que nunca deixa seu bot morrer

Se você rodar `python -m src.bot` direto num terminal SSH e sua internet piscar, o processo morre.
No Linux, usamos o **`systemd`** (veja o modelo pronto e comentado em [`templates/automacao-python/deploy/automacao.service`](../templates/automacao-python/deploy/automacao.service)):

- Se o programa travar, `Restart=always` levanta ele de novo em 5 segundos.
- Se faltar luz e o servidor religar, `WantedBy=multi-user.target` inicia seu bot sozinho no boot.
- Todos os `print()` vão automaticamente para um histórico organizado que você lê com `journalctl`.

### Os 4 comandos de operação que você vai usar toda semana:

```bash
# Ver se está vivo, quanta memória consome e há quanto tempo roda
sudo systemctl status automacao --no-pager

# Reiniciar depois de atualizar o código (git pull)
sudo systemctl restart automacao

# Acompanhar os logs ao vivo (Ctrl + C sai da visualização sem parar o bot!)
journalctl -u automacao -f

# Ver apenas logs da última 1 hora
journalctl -u automacao --since "1 hour ago" --no-pager
```

*(Para apps web como o `templates/web-fullstack`, você também pode empacotar com o `Dockerfile` já incluso lá dentro e subir com Docker!)*

---

## 3. Checklist de Segurança Obrigatório (Antes de Qualquer Push ou Deploy)

Segurança boa não é paranoia complicada — é fazer o básico **sempre**, sem exceção:

### 🔒 A. Código pode ser público; segredo e dado de cliente, NUNCA
- Senhas, chaves de API e tokens do Telegram vivem exclusivamente no arquivo **`.env`** com permissão restrita:
  ```bash
  chmod 600 .env   # só o seu usuário consegue ler o arquivo
  ```
- Antes de publicar qualquer repositório, passe um caçador automático de segredos vazados no histórico do Git, como o **[Gitleaks](https://github.com/gitleaks/gitleaks)**:
  ```bash
  gitleaks detect --source . -v
  ```

### 🛡️ B. Feche portas que não precisam ficar na rua
- Precisa acessar seu servidor Linux, painel interno ou banco de fora de casa? **Não abra portas no roteador!** Instale o **[Tailscale](https://tailscale.com/)** (gratuito para uso pessoal) no seu celular/notebook e no servidor: eles ganham um IP privado criptografado que só seus aparelhos enxergam.
- Ligue o firewall básico do Linux (`ufw`):
  ```bash
  sudo ufw default deny incoming
  sudo ufw default allow outgoing
  sudo ufw allow ssh
  sudo ufw enable
  ```

### 🙋‍♂️ C. Aprovação humana para ações destrutivas
- Seu bot detectou que um serviço parou ou quer apagar/alterar algo importante? Faça como no nosso exemplo do Módulo 03 e no agente SRE do `homelab`: **o robô diagnostica e manda um botão no Telegram pedindo seu OK**, em vez de sair reiniciando ou apagando coisas sozinho em loop.

---

## ✅ Parabéns! O que fazer agora?

Se você chegou até aqui fazendo as entregas práticas dos Módulos `00` a `05`, você já tem nas mãos **exatamente a caixa de ferramentas real** para construir sistemas web, automações 24/7 e agentes de IA com segurança.

Agora é hora de ganhar quilometragem construindo seus próprios projetos do zero! Escolha seu primeiro desafio em **[`desafios/PROJETOS-PRATICOS.md`](../desafios/PROJETOS-PRATICOS.md)**.
