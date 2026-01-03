/**
 * HTML to PDF Converter using Playwright
 * Converts worksheets to A4 PDF with proper page break handling
 * 
 * Usage: npx playwright test --project=chromium pdf_converter.js
 * Or: node pdf_converter.js <input_html_path> [output_pdf_path]
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

        // Inject CSS - force NO page break restrictions
        await page.addStyleTag({
            content: `
                @page {
                    size: A4;
                    margin: 15mm;
                }
                
                /* Force ALL elements to allow page breaks */
                * {
                    page-break-inside: auto !important;
                    break-inside: auto !important;
                    page-break-before: auto !important;
                    break-before: auto !important;
                    page-break-after: auto !important;
                    break-after: auto !important;
                }
                
                /* Hide print button */
                .no-print {
                    display: none !important;
                }
                
                /* Clean layout */
                .a4-page {
                    width: 100% !important;
                    min-height: auto !important;
                    box-shadow: none !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }
                
                .content-wrapper {
                    padding: 0 !important;
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
                top: '15mm',
                right: '15mm',
                bottom: '15mm',
                left: '15mm'
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
    console.log('Usage: node pdf_converter.js <input_html_path> [output_pdf_path]');
    process.exit(1);
}

convertToPDF(args[0], args[1]);
