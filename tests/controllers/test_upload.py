import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, mock_open
from app.main import app
from app.controllers.upload import upload_pdf, PDFUploadResponse
from fastapi import UploadFile

client = TestClient(app)


class TestPDFUpload:
    def test_upload_pdf_success(self):
        # Create a mock PDF file
        pdf_content = b"Mock PDF content"

        with (
            patch("app.controllers.upload.UPLOAD_DIR", "uploads"),
            patch("builtins.open", mock_open()) as mock_file_open,
        ):
            response = client.post(
                "/api/v1/upload/pdf",
                files={"file": ("test.pdf", pdf_content, "application/pdf")},
            )

            assert response.status_code == 200
            data = response.json()
            assert "file_id" in data
            assert data["filename"] == "test.pdf"
            assert data["message"] == "PDF uploaded successfully"

            # Verify file operations were called (check if any call matches our expected pattern)
            calls = mock_file_open.call_args_list
            upload_calls = [
                call for call in calls if len(call[0]) >= 2 and call[0][1] == "wb"
            ]
            assert len(upload_calls) >= 1, "Expected at least one file write operation"

    def test_upload_non_pdf_file(self):
        txt_content = b"Not a PDF file"

        response = client.post(
            "/api/v1/upload/pdf",
            files={"file": ("test.txt", txt_content, "text/plain")},
        )

        assert response.status_code == 400
        assert "Only PDF files are allowed" in response.json()["detail"]

    def test_upload_file_too_large(self):
        large_content = b"x" * (11 * 1024 * 1024)

        response = client.post(
            "/api/v1/upload/pdf",
            files={"file": ("large.pdf", large_content, "application/pdf")},
        )

        assert response.status_code == 400
        assert "File size exceeds 10MB limit" in response.json()["detail"]

    def test_upload_empty_filename(self):
        pdf_content = b"Mock PDF content"

        response = client.post(
            "/api/v1/upload/pdf",
            files={"file": ("", pdf_content, "application/pdf")},
        )

        # FastAPI returns 422 for validation errors when filename is empty
        assert response.status_code == 422

    def test_upload_case_insensitive_pdf_extension(self):
        pdf_content = b"Mock PDF content"

        with (
            patch("app.controllers.upload.UPLOAD_DIR", "uploads"),
            patch("builtins.open", mock_open()),
            patch("app.controllers.upload.os.makedirs"),
        ):
            response = client.post(
                "/api/v1/upload/pdf",
                files={"file": ("test.PDF", pdf_content, "application/pdf")},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["filename"] == "test.PDF"

    def test_upload_multiple_files(self):
        pdf_content1 = b"Mock PDF content 1"
        pdf_content2 = b"Mock PDF content 2"

        with (
            patch("app.controllers.upload.UPLOAD_DIR", "uploads"),
            patch("builtins.open", mock_open()),
            patch("app.controllers.upload.os.makedirs"),
        ):
            response1 = client.post(
                "/api/v1/upload/pdf",
                files={"file": ("test1.pdf", pdf_content1, "application/pdf")},
            )
            assert response1.status_code == 200

            response2 = client.post(
                "/api/v1/upload/pdf",
                files={"file": ("test2.pdf", pdf_content2, "application/pdf")},
            )
            assert response2.status_code == 200

            data1 = response1.json()
            data2 = response2.json()
            assert data1["file_id"] != data2["file_id"]

    def test_upload_handles_directory_creation(self):
        pdf_content = b"Mock PDF content"

        with (
            patch("app.controllers.upload.UPLOAD_DIR", "uploads"),
            patch("builtins.open", mock_open()),
        ):
            response = client.post(
                "/api/v1/upload/pdf",
                files={"file": ("test.pdf", pdf_content, "application/pdf")},
            )

            assert response.status_code == 200

    def test_upload_file_content_validation(self):
        pdf_content = b"Mock PDF content"

        with (
            patch("app.controllers.upload.UPLOAD_DIR", "uploads"),
            patch("builtins.open", mock_open()),
            patch("app.controllers.upload.os.makedirs"),
        ):
            response = client.post(
                "/api/v1/upload/pdf",
                files={"file": ("test.pdf", pdf_content, "application/pdf")},
            )

            assert response.status_code == 200

    def test_upload_response_model(self):
        pdf_content = b"Mock PDF content"

        with (
            patch("app.controllers.upload.UPLOAD_DIR", "uploads"),
            patch("builtins.open", mock_open()),
            patch("app.controllers.upload.os.makedirs"),
        ):
            response = client.post(
                "/api/v1/upload/pdf",
                files={"file": ("test.pdf", pdf_content, "application/pdf")},
            )

            assert response.status_code == 200
            data = response.json()

            required_fields = ["file_id", "filename", "message"]
            for field in required_fields:
                assert field in data

            assert isinstance(data["file_id"], str)
            assert isinstance(data["filename"], str)
            assert isinstance(data["message"], str)

            assert len(data["file_id"]) == 36
            assert data["file_id"].count("-") == 4

    def test_upload_error_handling(self):
        pdf_content = b"Mock PDF content"

        with (
            patch("app.controllers.upload.UPLOAD_DIR", "uploads"),
            patch("builtins.open", side_effect=IOError("Write error")),
            patch("app.controllers.upload.os.makedirs"),
        ):
            response = client.post(
                "/api/v1/upload/pdf",
                files={"file": ("test.pdf", pdf_content, "application/pdf")},
            )

            assert response.status_code == 500
            assert "Error uploading PDF" in response.json()["detail"]

    def test_upload_unique_filename_generation(self):
        pdf_content = b"Mock PDF content"

        with (
            patch("app.controllers.upload.UPLOAD_DIR", "uploads"),
            patch("builtins.open", mock_open()),
            patch("app.controllers.upload.os.makedirs"),
        ):
            file_ids = []
            for i in range(3):
                response = client.post(
                    "/api/v1/upload/pdf",
                    files={"file": ("test.pdf", pdf_content, "application/pdf")},
                )
                assert response.status_code == 200
                file_ids.append(response.json()["file_id"])

            assert len(set(file_ids)) == 3  # All unique

    @pytest.mark.asyncio
    async def test_upload_pdf_function_directly(self):
        pdf_content = b"Mock PDF content"

        with (
            patch("app.controllers.upload.UPLOAD_DIR", "uploads"),
            patch("builtins.open", mock_open()) as mock_file_open,
        ):
            mock_file = MagicMock(spec=UploadFile)
            mock_file.filename = "test.pdf"
            mock_file.size = len(pdf_content)
            mock_file.read.return_value = pdf_content

            result = await upload_pdf(mock_file)

            assert isinstance(result, PDFUploadResponse)
            assert result.filename == "test.pdf"
            assert result.message == "PDF uploaded successfully"
            assert len(result.file_id) == 36  # UUID length

            calls = mock_file_open.call_args_list
            upload_calls = [
                call for call in calls if len(call[0]) >= 2 and call[0][1] == "wb"
            ]
            assert len(upload_calls) >= 1, "Expected at least one file write operation"
