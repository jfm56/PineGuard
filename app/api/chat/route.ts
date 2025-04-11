import { NextRequest } from 'next/server';
import OpenAI from 'openai';

if (!process.env.OPENAI_API_KEY) {
  throw new Error('Missing environment variable OPENAI_API_KEY');
}

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export const runtime = 'edge';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { messages } = body;
    if (!messages) {
      return new Response('Messages array is required', { status: 400 });
    }

    // Check for API key
    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      console.error('No API key provided');
      return new Response('No API key provided', { status: 500 });
    }

    // Create a streaming response
    const stream = new ReadableStream({
      async start(controller) {
        try {
          const systemPrompt = `You are Firefighter Bill, an expert in wildfire prevention and response in the New Jersey Pinelands.

Your expertise includes:
- Wildfire prevention and safety
- Fire risk assessment
- Emergency preparedness
- Evacuation procedures
- Local fire history
- Pinelands ecosystem and fire ecology

Respond in a friendly, helpful manner while maintaining professionalism. Keep responses focused on wildfire-related topics.`;

          const response = await openai.chat.completions.create({
            messages: [
              { role: 'system', content: systemPrompt },
              ...messages.map((msg: any) => ({
                role: msg.role,
                content: msg.content,
              })),
            ],
            model: process.env.LLM_MODEL || 'gpt-3.5-turbo',
            stream: true,
          });

          for await (const chunk of response) {
            if (chunk.choices[0]?.delta?.content) {
              const queue = new TextEncoder().encode(chunk.choices[0].delta.content);
              controller.enqueue(queue);
            }
          }
          controller.close();
        } catch (error) {
          console.error('Error in stream:', error);
          controller.error(error);
        }
      },
    });

    return new Response(stream);
  } catch (error) {
    console.error('Error:', error);
    return new Response('Internal Server Error', { status: 500 });
  }
}
