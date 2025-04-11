import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(req: NextRequest) {
  try {
    const weatherData = await req.json();

    const response = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: `You are a wildfire risk assessment expert specializing in weather conditions.
          Analyze weather data and provide clear, actionable insights about fire risk levels.
          Include specific precautions based on current conditions.`
        },
        {
          role: "user",
          content: `Analyze these weather conditions for fire risk:
          - Temperature: ${weatherData.temperature}°F
          - Humidity: ${weatherData.humidity}%
          - Wind Speed: ${weatherData.windSpeed} mph
          - Wind Direction: ${weatherData.windDirection}
          - Precipitation: ${weatherData.precipitation} inches
          
          Provide:
          1. Current fire risk level
          2. Specific concerns based on conditions
          3. Recommended precautions
          4. Forecast implications`
        }
      ],
      max_tokens: 500,
    });

    return NextResponse.json({ 
      analysis: response.choices[0].message.content 
    });
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json(
      { error: 'Failed to analyze weather risk' },
      { status: 500 }
    );
  }
}
