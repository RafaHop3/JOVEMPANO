# Guia de Configuração: Cloudflare Pages e WAF (Cyber Safety de Borda)

Para o **JovemPano**, optamos por uma estratégia robusta: SSG (Static Site Generation), onde o framework **Astro** converte todas as matérias previamente processadas em arquivos puramente HTML durante o *build*. Para blindar completamente essa vitrine, protegeremos a borda com **Cloudflare**.

## 1. Hospedagem Rápida via Cloudflare Pages
Para a hospedagem grátis, rápida e nativamente imune a ataques back-end:
1. Faça login na sua conta do [Cloudflare Dashboard](https://dash.cloudflare.com/).
2. Acesse **Workers & Pages** -> **Create application** -> **Pages** -> **Connect to Git** (ou Direct Upload do diretório `dist`).
3. Conecte o repositório GitHub onde enviará essa base de código.
4. **Build settings**:
   - **Framework preset**: `Astro`
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
   - **Root directory**: `/frontend` (caso o repositório englobe backend e frontend juntos)
5. Clique em **Save and Deploy**. 

## 2. Regras de Segurança (WAF)
O site estático não possuirá vulnerabilidades de injeção direta no navegador do usuário, mas ainda blindaremos contra Scraping (plágio das suas notícias), botnets e DDoS L7. Acesse o seu domínio principal no painel e vá na seção **Security**:

### A) Super Bot Fight Mode
- Em **Security** -> **Bots**: Ative o **Bot Fight Mode**. Essa função emite verificações matemáticas imperceptíveis contra acessos mecanizados, bloqueando raspadores de conteúdo imediatamente.

### B) Rate Limiting (Proteção Anti-DDoS)
Previne exaustão de banda. Crie uma regra customizada na aba WAF:
- **Expressão Match**: `(http.request.uri.path contains "/")`
- **Ação**: Block
- **Frequência**: Acima de `100 requests / 10s` vindos do mesmo IP.

### C) WAF Custom Block e Hotlinking
- Se o público é puramente brasileiro, crie uma WAF rule obrigando IPs internacionais a passarem por validação: `(ip.geoip.country ne "BR")` -> **Action**: *Managed Challenge*.
- Em **Scrape Shield**, ative a proteção de *Hotlink* para evitar que outros sites consumam suas imagens hospedadas, gerando picos de tráfego inúteis.
