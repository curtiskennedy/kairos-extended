const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const port = 3000;


const pdfFolderPath = path.join(__dirname, 'pdf');
const textFolderPath = path.join(__dirname, 'text');


app.use('/pdf', express.static(pdfFolderPath));


app.get('/', (req, res) => {
  fs.readdir(pdfFolderPath, (err, files) => {
    if (err) {
      return res.status(500).send('Unable to read PDF files.');
    }

    const pdfFiles = files.filter(file => file.endsWith('.pdf'));

    let fileListHtml = '<h1>List of PDF Files</h1><ul>';
    pdfFiles.forEach(file => {
      fileListHtml += `<li><a href="/view-pdf/${file}">${file}</a></li>`;
    });
    fileListHtml += '</ul>';
    res.send(fileListHtml);
  });
});


app.get('/view-pdf/:filename', (req, res) => {
  const { filename } = req.params;

  const pdfFilePath = path.join(pdfFolderPath, filename);
  const textFilePath = path.join(textFolderPath, filename.replace('.pdf', '.txt'));

  if (fs.existsSync(pdfFilePath)) {
    fs.readFile(textFilePath, 'utf-8', (err, textContent) => {
      if (err) {
        textContent = 'No text content available for this file.'; // Fallback if no .txt file
      }


      res.send(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>View PDF: ${filename}</title>
          <style>
            body {
              font-family: Arial, sans-serif;
              margin: 0;
              padding: 0;
              box-sizing: border-box;
              display: flex;
              flex-direction: column;
              align-items: center;
              background-color: #f4f4f4;
            }
            h1 {
              margin-top: 20px;
            }
            .container {
              max-width: 100%;
              width: 80%;
              margin: 20px;
              display: flex;
              flex-direction: column;
              align-items: center;
              justify-content: center;
            }
            .pdf-container {
              width: 100%;
              height: 60vh; 
              overflow: hidden;
              margin-bottom: 20px;
            }
            embed {
              width: 100%;
              height: 100%;
              border: none;
              object-fit: contain; 
            }
            .text-content {
              width: 100%;
              max-width: 100%;
              padding: 20px;
              background-color: white;
              border-radius: 8px;
              box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
              font-size: 14px;
              line-height: 1.5;
              max-height: 50vh;
              overflow-y: auto;
              white-space: normal; 
              word-wrap: break-word; 
              word-break: break-word; 
            }
            a {
              text-decoration: none;
              color: #007bff;
              font-size: 16px;
              margin-top: 20px;
            }
          </style>
        </head>
        <body>
          <div class="container">
            <h1>Viewing: ${filename}</h1>

            <!-- PDF Viewer -->
            <div class="pdf-container">
              <embed src="/pdf/${filename}" type="application/pdf" style="object-fit: contain;">
            </div>

            <!-- Text Content from .txt file -->
            <div class="text-content">
              <div>${textContent}</div> <!-- Replace <pre> with <div> for wrapping -->
            </div>

            <a href="/">Back to list</a> <!-- Link to go back to the list -->
          </div>
        </body>
        </html>
      `);
    });
  } else {
    res.status(404).send('PDF file not found');
  }
});

// Start the server on port 3000
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
