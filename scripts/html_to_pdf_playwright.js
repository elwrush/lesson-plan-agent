/**
 * HTML to PDF Converter using Playwright
 * Converts worksheets to A4 PDF with proper page break handling
 * 
 * Usage: npx playwright test --project=chromium html_to_pdf_playwright.js
 * Or: node html_to_pdf_playwright.js <input_html_path> [output_pdf_path]
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function convertToPDF(inputPath, outputPath) {
    // Resolve absolute paths
    const absoluteInputPath = path.resolve(inputPath);
    const absoluteOutputPath = outputPath
        ? path.resolve(outputPath)
        : absoluteInputPath.replace(/\.html$/i, '.pdf');

    if (!fs.existsSync(absoluteInputPath)) {
        console.error(`Error: Input file not found: ${absoluteInputPath}`);
        process.exit(1);
    }

    console.log(`Converting: ${absoluteInputPath}`);
    console.log(`Output: ${absoluteOutputPath}`);

    const browser = await chromium.launch();

    try {
        const page = await browser.newPage();

        // Navigate to the HTML file
        const fileUrl = `file:///${absoluteInputPath.replace(/\\/g, '/')}`;
        await page.goto(fileUrl, { waitUntil: 'networkidle' });

        // Inject CSS for print-specific page break handling
        await page.addStyleTag({
            content: `
                @page {
                    size: A4;
                    margin: 0;
                }
                
                /* Prevent page breaks inside tasks */
                section {
                    page-break-inside: avoid !important;
                    break-inside: avoid !important;
                }
                
                /* Allow page breaks within reading text */
                .reading-text {
                    page-break-inside: auto !important;
                    break-inside: auto !important;
                }
                
                /* Prevent orphaned paragraphs in reading text */
                .reading-text p {
                    page-break-inside: avoid !important;
                    break-inside: avoid !important;
                    orphans: 3;
                    widows: 3;
                }
                
                /* Keep task headers with their content */
                section > div:first-child {
                    page-break-after: avoid !important;
                    break-after: avoid !important;
                }
                
                /* Allow page breaks before tasks */
                section {
                    page-break-before: auto !important;
                    break-before: auto !important;
                }
                
                /* Hide print button */
                .no-print {
                    display: none !important;
                }
                
                /* Ensure clean A4 page layout */
                .a4-page {
                    width: 210mm !important;
                    min-height: auto !important;
                    box-shadow: none !important;
                    margin: 0 !important;
                }
                
                body {
                    background: white !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }
            `
        });

        // Generate PDF with A4 dimensions
        await page.pdf({
            path: absoluteOutputPath,
            format: 'A4',
            printBackground: true,
            margin: {
                top: '0',
                right: '0',
                bottom: '0',
                left: '0'
            },
            preferCSSPageSize: true
        });

        console.log(`✅ PDF created successfully: ${absoluteOutputPath}`);

    } catch (error) {
        console.error('Error generating PDF:', error);
        process.exit(1);
    } finally {
        await browser.close();
    }
}

// Main execution
const args = process.argv.slice(2);
if (args.length === 0) {
    console.log('Usage: node html_to_pdf_playwright.js <input_html_path> [output_pdf_path]');
    console.log('Example: node html_to_pdf_playwright.js worksheet.html worksheet.pdf');
    process.exit(1);
}

convertToPDF(args[0], args[1]);
