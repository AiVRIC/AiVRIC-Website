import { NextResponse } from 'next/server';
import nodemailer from 'nodemailer';

export async function POST(req: Request) {
  try {
    const form = await req.formData();
    const payload = JSON.parse(form.get('payload') as string || '{}');

    const SMTP_HOST = process.env.SMTP_HOST;
    if(!SMTP_HOST){
      // dev mode: log and return success
      // eslint-disable-next-line no-console
      console.log('Email payload (dev):', payload);
      return NextResponse.json({ ok: true, dev: true });
    }

    const transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: Number(process.env.SMTP_PORT || 587),
      secure: process.env.SMTP_SECURE === 'true',
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
      }
    });

    await transporter.sendMail({
      from: process.env.SMTP_FROM || 'no-reply@aivric.local',
      to: (form.get('to') as string) || process.env.DEV_EMAIL || 'dev@example.com',
      subject: 'AiVRIC Configurator Results',
      text: JSON.stringify(payload, null, 2)
    });

    return NextResponse.json({ ok: true });
  } catch (err) {
    return NextResponse.json({ ok: false, error: String(err) }, { status: 500 });
  }
}
