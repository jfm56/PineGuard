import { NextRequest } from 'next/server';
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export const runtime = 'edge';

export async function POST(req: NextRequest) {
  try {
    const planDetails = await req.json();

    const response = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: `You are an emergency planning expert specializing in wildfire evacuation plans. 
          Create detailed, personalized evacuation plans based on the provided information.
          Include specific routes, preparation steps, and safety considerations.`
        },
        {
          role: "user",
          content: `Create a detailed evacuation plan for:
          - Address: ${planDetails.address}
          - Family Size: ${planDetails.familySize}
          - Pets: ${planDetails.hasPets ? 'Yes' : 'No'}
          - Special Needs: ${planDetails.hasSpecialNeeds ? 'Yes - ' + planDetails.specialNeedsDetails : 'No'}
          
          Include:
          1. Preparation steps
          2. Essential items to pack
          3. Primary and secondary evacuation routes
          4. Emergency contact information
          5. Special considerations for the specific location`
        }
      ],
      max_tokens: 1000,
    });

    return new Response(
      JSON.stringify({ 
        plan: response.choices[0].message.content 
      }),
      { 
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  } catch (error) {
    console.error('Error:', error);
    return new Response(
      JSON.stringify({ error: 'Failed to generate plan' }),
      { status: 500 }
    );
  }
}
