import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';

const interests = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/interests' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    order: z.number(),
    visual: z.enum(['packing', 'life', 'neural', 'crypto', 'chess', 'fractal', 'gear']).optional(),
  }),
});
const articles = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/articles' }),
  schema: z
    .object({
      title: z.string(),
      description: z.string(),
      type: z.enum(['research', 'project']),
      topics: z.array(z.string()).min(1),
      tags: z.array(z.string()).default([]),
      status: z.enum(['demonstrated', 'implemented', 'experimental', 'candidate', 'ongoing']),
      featured: z.boolean().default(false),
      showPreview: z.boolean().optional(),
      presentationOrder: z.number().default(0),
      date: z.coerce.date(),
      updated: z.coerce.date().optional(),
      draft: z.boolean().default(false),
      github: z.url().optional(),
      demo: z.url().optional(),
      demoNote: z.string().optional(),
      image: z.string().optional(),
      imageAlt: z.string().optional(),
      imageCredit: z.string().optional(),
      imageSource: z.url().optional(),
      visual: z
        .enum(['packing', 'life', 'neural', 'crypto', 'chess', 'fractal', 'gear'])
        .default('packing'),
      sources: z.array(z.object({ label: z.string(), url: z.url() })).min(1),
    })
    .transform((data) => ({ ...data, showPreview: data.showPreview ?? Boolean(data.image) })),
});
export const collections = { interests, articles };
