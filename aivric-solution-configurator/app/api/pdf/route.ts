import PDFDocument from 'pdfkit';

export async function POST(req: Request) {
  try {
    let payload: any = {};
    const contentType = req.headers.get('content-type') || '';
    if (contentType.includes('application/json')) payload = await req.json();
    else {
      const form = await req.formData();
      payload = JSON.parse((form.get('payload') as string) || '{}');
    }

    const doc = new PDFDocument({ size: 'A4', margin: 50 });
    const chunks: Uint8Array[] = [];

    doc.on('data', (chunk) => chunks.push(chunk));
    const endPromise = new Promise<Buffer>((resolve) => doc.on('end', () => resolve(Buffer.concat(chunks))));

    doc.fontSize(18).text('AiVRIC Solution Configurator Results', { align: 'center' });
    doc.moveDown();

    const cfg = payload?.data ?? {};
    const rec = payload?.rec ?? {};

    doc.fontSize(12).text('Summary', { underline: true });
    doc.moveDown(0.25);
    doc.fontSize(10).text(`Persona: ${cfg.org?.persona ?? 'N/A'}`);
    doc.text(`Organization size: ${cfg.org?.size ?? 'N/A'}`);
    doc.text(`Industry: ${cfg.org?.industry ?? 'N/A'}`);
    doc.moveDown();

    doc.fontSize(12).text('Recommendation', { underline: true });
    doc.moveDown(0.25);
    doc.fontSize(11).text(`Tier: ${rec.tier ?? 'N/A'}`);
    doc.text(`Score: ${rec.score ?? 0}`);
    doc.moveDown();

    doc.fontSize(12).text('Modules', { underline: true });
    doc.moveDown(0.25);
    if (Array.isArray(rec.modules) && rec.modules.length) {
      rec.modules.forEach((m: any) => {
        doc.list([`${m.name} — ${Array.isArray(m.outcomes) ? m.outcomes.join(', ') : ''}`], { bulletIndent: 10 });
      });
    } else {
      doc.fontSize(10).text('No modules selected');
    }
    doc.moveDown();

    doc.fontSize(12).text('Rationale', { underline: true });
    doc.moveDown(0.25);
    if (Array.isArray(rec.rationale)) {
      rec.rationale.forEach((r: any) => {
        const mark = r.matched ? '+' : '-';
        doc.fontSize(10).text(`${mark} ${r.description} ${r.matched ? `(+${r.score})` : ''}`);
      });
    }
    doc.moveDown();

    doc.fontSize(12).text('Estimated Deployment', { underline: true });
    doc.moveDown(0.25);
    const timeline = (rec.tier === 'Best') ? '8-16 weeks (includes integration, onboarding, tuning).' : (rec.tier === 'Better') ? '6-10 weeks (standard integrations, some tuning).' : '4-8 weeks (core modules, minimal integrations).';
    doc.fontSize(10).text(timeline);
    doc.moveDown();

    doc.fontSize(12).text("What we'll need from the customer", { underline: true });
    doc.moveDown(0.25);
    doc.list([
      'Admin access to cloud accounts (least privilege)',
      'Designated security contact',
      'Time for onboarding workshops (2-5 days)'
    ]);
    doc.end();

    const buffer = await endPromise;

    return new Response(buffer, {
      status: 200,
      headers: { 'Content-Type': 'application/pdf', 'Content-Disposition': 'attachment; filename="aivric-results.pdf"' }
    });
  } catch (err) {
    return new Response(JSON.stringify({ ok: false, error: String(err) }), { status: 500, headers: { 'Content-Type': 'application/json' } });
  }
}
