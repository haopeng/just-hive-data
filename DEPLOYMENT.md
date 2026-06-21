# Just Hive Data Website Deployment

## Current production deployment

- Vercel project: `just-hive-data`
- Production URL: https://just-hive-data.vercel.app
- Vercel inspect URL: https://vercel.com/haopengz-6386s-projects/just-hive-data/6FbTs1ggQAGARM33t79zwKdDfbxM

## GitHub Pages deployment

The site also includes a GitHub Pages workflow:

- Workflow file: `.github/workflows/deploy-pages.yml`
- Build command: `npm run build`
- Publish directory: `dist`
- Expected GitHub Pages URL after the workflow completes: `https://haopeng.github.io/just-hive-data/`

The site uses relative asset URLs and `base: './'` in `vite.config.js`, so it works under the GitHub project path and under a custom domain.

## Current domain state

`just-hive-data.com` is using Cloudflare nameservers:

- `elsa.ns.cloudflare.com`
- `boyd.ns.cloudflare.com`

Current DNS observed during deployment:

- `just-hive-data.com` returns Cloudflare IPs and redirects to `https://www.just-hive-data.com/`
- `www.just-hive-data.com` is a CNAME to `ghs.googlehosted.com`

That means the domain is still wired to the old Google Sites setup.

## Recommended custom-domain cutover

Recommended primary domain: `www.just-hive-data.com`, with `just-hive-data.com` redirecting to `www`.

### Option A: GitHub Pages

1. In GitHub, open repository `haopeng/just-hive-data`.
2. Go to Settings -> Pages.
3. Confirm the source is GitHub Actions.
4. Under Custom domain, set `www.just-hive-data.com`.
5. In Cloudflare DNS, replace the old Google Sites CNAME:
   - Type: `CNAME`
   - Name: `www`
   - Target: `haopeng.github.io`
   - Proxy status: DNS only
6. For the apex domain, either keep the current Cloudflare redirect from `just-hive-data.com` to `www.just-hive-data.com`, or use GitHub Pages apex records:
   - Type: `A`, Name: `@`, Target: `185.199.108.153`
   - Type: `A`, Name: `@`, Target: `185.199.109.153`
   - Type: `A`, Name: `@`, Target: `185.199.110.153`
   - Type: `A`, Name: `@`, Target: `185.199.111.153`
7. Remove or disable any old Google Sites DNS records or Cloudflare redirect/page rules that still send traffic to Google.

### Option B: Vercel

1. In Vercel, open project `just-hive-data`.
2. Go to Settings -> Domains.
3. Add `www.just-hive-data.com`.
4. Add `just-hive-data.com` as well, so Vercel can manage the apex/non-www redirect behavior.
5. If Vercel asks for domain verification, copy the TXT record it gives you into Cloudflare DNS.
6. In Cloudflare DNS, replace the old Google Sites CNAME:
   - Type: `CNAME`
   - Name: `www`
   - Target: the exact Vercel CNAME value shown in the Vercel project Domains screen
   - Proxy status: DNS only
7. For the apex domain, either:
   - keep the existing Cloudflare redirect from `just-hive-data.com` to `www.just-hive-data.com`, or
   - remove the redirect and add the A record shown by Vercel for `just-hive-data.com`.
8. Remove or disable any old Google Sites DNS records or Cloudflare redirect/page rules that still send traffic to Google.

## Fast redirect-only option

If you do not need the site to appear under the custom domain immediately, you can create a Cloudflare Redirect Rule:

- Match hostnames `just-hive-data.com` and `www.just-hive-data.com`
- Redirect to `https://just-hive-data.vercel.app`
- Status code: `301` or `302`

This is simpler, but the browser will show the `vercel.app` URL after redirecting. The recommended production setup is the custom-domain cutover above.
