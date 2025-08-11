#!/usr/bin/env python3
"""
MCP HTTP 橋梁包裝器 - 只負責協議轉換
"""

import json
import logging
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

# 設定日誌
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MCPHTTPHandler(BaseHTTPRequestHandler):
    """MCP HTTP 處理器 - 純橋梁功能"""

    def do_GET(self):
        """處理 GET 請求 - 重定向到面試系統"""
        if self.path == "/":
            self.send_response(302)
            self.send_header("Location", "http://localhost:5000")
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        """處理 POST 請求 - 轉發給 MCP 服務"""
        if self.path == "/api/chat":
            try:
                # 讀取請求內容
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode("utf-8"))

                # 轉發給 MCP 服務（這裡應該調用你的 MCP 工具）
                result = self.forward_to_mcp(data)

                # 返回結果
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))

            except Exception as e:
                logger.error(f"處理請求失敗: {e}")
                self.send_response(500)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"error": str(e)}, ensure_ascii=False).encode("utf-8")
                )
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": "端點不存在"}, ensure_ascii=False).encode("utf-8")
            )

    def forward_to_mcp(self, data):
        """轉發請求給 MCP 服務"""
        try:
            # 這裡應該調用你的 MCP 工具，而不是處理業務邏輯
            message = data.get("message", "")

            # 簡單的轉發邏輯，實際應該調用 MCP 服務
            return {
                "response": f"MCP 橋梁收到訊息: {message}",
                "status": "forwarded",
                "service": "mcp_bridge",
            }
        except Exception as e:
            logger.error(f"MCP 轉發失敗: {e}")
            return {"error": f"MCP 轉發失敗: {str(e)}"}

    def do_OPTIONS(self):
        """處理 CORS 預檢請求"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def main():
    """主函數"""
    port = 8080
    try:
        server = HTTPServer(("localhost", port), MCPHTTPHandler)
        logger.info(f"🚀 啟動 MCP HTTP 橋梁 - http://localhost:{port}")
        logger.info("按 Ctrl+C 停止伺服器")
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("伺服器被用戶中斷")
    finally:
        logger.info("伺服器關閉")


if __name__ == "__main__":
    main()
