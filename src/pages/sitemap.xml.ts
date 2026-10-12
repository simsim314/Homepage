import { getContent, href } from '../lib/content';
export async function GET() {
  const { articles, interests } = await getContent();
  const paths = [
    '',
    'interests/',
    'research/',
    'projects/',
    'about/',
    'search/',
    ...articles.map((a) => `articles/${a.id}/`),
    ...interests.map((i) => `interests/${i.id}/`),
  ];
  const body = `<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${paths.map((p) => `<url><loc>https://simsim314.github.io${href(p)}</loc></url>`).join('')}</urlset>`;
  return new Response(body, { headers: { 'Content-Type': 'application/xml' } });
}
