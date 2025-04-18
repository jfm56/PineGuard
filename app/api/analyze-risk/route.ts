import { NextRequest } from 'next/server';
import OpenAI from 'openai';

interface ImageContent {
  type: 'image_url';
  image_url: { url: string };
}

interface TextContent {
  type: 'text';
  text: string;
}

type Content = TextContent | ImageContent;

interface SystemMessage {
  role: 'system';
  content: string;
}

interface UserMessage {
  role: 'user';
  content: Content[];
}

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export const runtime = 'edge';

export async function POST(req: NextRequest): Promise<Response> {
  try {
    const { image } = await req.json() as { image: string };

    const messages: (SystemMessage | UserMessage)[] = [
      {
        role: "system",
        content: "You are a wildfire safety expert analyzing property images for fire risks. Focus on identifying potential hazards and providing specific, actionable recommendations for improving safety."
      },
      {
        role: "user",
        content: [
          { type: "text", text: "Analyze this property image for wildfire risks and provide specific safety recommendations." },
          { type: "image_url", image_url: { url: image } }
        ],
      },
    ];

    const response = await openai.chat.completions.create({
      model: "gpt-4-vision-preview",
      messages,
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

    return new Response(
      JSON.stringify({ error: error instanceof Error ? error.message : 'Failed to analyze image' }),
      { status: 500 }
    );
  }
}
