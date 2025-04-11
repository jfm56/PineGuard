import './globals.css';
import 'leaflet/dist/leaflet.css';
import Script from 'next/script';

export const metadata = {
  title: 'Pinelands Wildfire Assistant',
  description: 'Get expert advice on wildfire prevention and safety in the New Jersey Pinelands',
}



export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}): JSX.Element {

  return (
    <html lang="en">
      <head>
        <link
          rel="stylesheet"
          href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
          crossOrigin=""
        />
        <Script
          src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
          integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
          crossOrigin=""
          strategy="beforeInteractive"
        />
      </head>
      <body className="bg-gray-100">
        <div className="fixed top-0 right-0 z-50">
          <a 
            href="/api-test" 
            target="_blank"
            className="bg-gray-800 text-white px-4 py-2 text-sm rounded-bl-lg hover:bg-gray-700 transition-colors"
          >
            Test API Keys
          </a>
        </div>
        {children}
      </body>
    </html>
  )
}
