import { NextRequest } from 'next/server';
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export const runtime = 'edge';

export async function POST(req: NextRequest): Promise<Response> {
  try {
    const { image } = await req.json();

    const response = await openai.chat.completions.create({
      model: "gpt-4-vision-preview",
      messages: [
        {
          role: "system",
          content: "You are a wildfire safety expert analyzing property images for fire risks. Focus on identifying potential hazards and providing specific, actionable recommendations for improving safety."
        },
        {
          role: "user",
          content: [
            { type: "text", text: "Analyze this property image for wildfire risks and provide specific safety recommendations." },
            { type: "image_url", image_url: image }
          ],
        },
      ],
      max_tokens: 500,
    });

    return new Response(
      JSON.stringify({ 
        analysis: response.choices[0].message.content 
      }),
      { 
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  } catch (error) {
    console.error('Error:', error);
    return new Response(
      JSON.stringify({ error: 'Failed to analyze image' }),
      { status: 500 }
    );
  }
}
