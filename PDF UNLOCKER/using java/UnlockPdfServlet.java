import com.itextpdf.text.pdf.PdfReader;
import com.itextpdf.text.pdf.PdfStamper;
import com.itextpdf.text.pdf.PdfWriter;
import java.io.*;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/unlockpdf")
public class UnlockPdfServlet extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        try {
            // Retrieve the PDF file and password from the request
            Part filePart = request.getPart("pdfFile");
            String password = request.getParameter("password");

            // Create a temporary file to store the unlocked PDF
            File unlockedFile = File.createTempFile("unlocked_", ".pdf");
            FileOutputStream unlockedPdfStream = new FileOutputStream(unlockedFile);

            // Read the original PDF file and unlock it with the provided password
            InputStream pdfStream = filePart.getInputStream();
            PdfReader reader = new PdfReader(pdfStream);
            PdfStamper stamper = new PdfStamper(reader, unlockedPdfStream);
            stamper.setEncryption(null, password.getBytes(), 0, PdfWriter.STANDARD_ENCRYPTION_128);

            stamper.close();
            reader.close();

            // Set the response content type
            response.setContentType("application/pdf");

            // Write the unlocked PDF as a response
            FileInputStream unlockedPdfInputStream = new FileInputStream(unlockedFile);
            OutputStream responseOutputStream = response.getOutputStream();

            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = unlockedPdfInputStream.read(buffer)) != -1) {
                responseOutputStream.write(buffer, 0, bytesRead);
            }
//updating...

            unlockedPdfInputStream.close();
            responseOutputStream.flush();
        } catch (Exception e) {
            response.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR, "Error: " + e.getMessage());
        }
    }
}
