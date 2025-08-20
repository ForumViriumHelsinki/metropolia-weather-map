import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({ 
    status: 'healthy', 
    service: 'nextjs-client',
    timestamp: new Date().toISOString()
  })
}