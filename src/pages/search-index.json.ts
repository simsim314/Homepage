import { getContent, articleHref } from '../lib/content';
export async function GET() {
  const { articles, interests } = await getContent();
  return Response.json(
    articles.map((a) => ({
      title: a.data.title,
      description: a.data.description,
      url: articleHref(a),
      text: (a.body || '').replace(/<[^>]+>/g, ' ').replace(/[\[\]#*`]/g, ' '),
      topics: a.data.topics.map((t) => `${t} ${interests.find((i) => i.id === t)!.data.title}`),
      tags: a.data.tags,
    })),
  );
}
