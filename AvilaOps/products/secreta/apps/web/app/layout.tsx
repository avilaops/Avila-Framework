import Script from "next/script";

export default function RootLayout({ children }: { children: React.ReactNode }) {
    const measurementId = process.env.NEXT_PUBLIC_GA4_ID || "G-PULSE-DEV";
    const gtmId = process.env.NEXT_PUBLIC_GTM_ID || "GTM-P9142SM";

    return (
        <html lang="pt-BR">
            <head>
                {/* Google Tag Manager */}
                <Script
                    id="gtm-script"
                    strategy="afterInteractive"
                    dangerouslySetInnerHTML={{
                        __html: `
              (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
              new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
              j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
              'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
              })(window,document,'script','dataLayer','${gtmId}');
            `,
                    }}
                />

                {/* GA4 Script */}
                <Script
                    strategy="afterInteractive"
                    src={`https://www.googletagmanager.com/gtag/js?id=${measurementId}`}
                />
                <Script
                    id="ga4-init"
                    strategy="afterInteractive"
                    dangerouslySetInnerHTML={{
                        __html: ` 
              window.dataLayer = window.dataLayer || []; 
              function gtag(){dataLayer.push(arguments);} 
              window.gtag = gtag;
              gtag('config', '${measurementId}');
            `
                    }}
                />
            </head>
            <body>
                {/* Google Tag Manager (noscript) */}
                <noscript>
                    <iframe
                        src={`https://www.googletagmanager.com/ns.html?id=${gtmId}`}
                        height="0"
                        width="0"
                        style={{ display: 'none', visibility: 'hidden' }}
                    />
                </noscript>
                {children}
            </body>
        </html>
    );
}