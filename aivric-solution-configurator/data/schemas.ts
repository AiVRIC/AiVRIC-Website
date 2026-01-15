import { z } from 'zod';

export const orgSchema = z.object({
  size: z.number().min(1).optional(),
  industry: z.string().optional(),
  persona: z.enum(['CISO','IT Ops','GRC','Product']).optional()
});

export const postureSchema = z.object({
  siem: z.enum(['Yes','No']).optional(),
  edr: z.enum(['Yes','No']).optional(),
  mttd: z.number().optional()
});

export const prioritiesSchema = z.object({
  top: z.array(z.string()).optional()
});

export const envSchema = z.object({
  cloud: z.string().optional(),
  idp: z.string().optional()
});

export const constraintsSchema = z.object({
  budget: z.number().optional(),
  timeline: z.number().optional()
});

export const stepSchemas: Record<string, any> = {
  org: orgSchema,
  posture: postureSchema,
  priorities: prioritiesSchema,
  env: envSchema,
  constraints: constraintsSchema
};

export function getSchemaForStep(stepId: string){
  return stepSchemas[stepId] ?? z.object({});
}
