# bot_hacker_gtd.py
import os
import asyncio
import time
import random
from datetime import datetime
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Lấy token từ biến môi trường (NHỚ ĐẶT BIẾN MÔI TRƯỜNG BOT_TOKEN)
BOT_TOKEN = '8735966417:AAH-wEaDb73q0Q-c72r1aswN-XGioqIsE50'
# Các hằng số key (ẩn trong code)
KEY1 = "KEYGTDVIPKEY1HACMERTOL99"
KEY2 = "ADMINVIPKEY2GTDSIEUCAP99FT"

# Các trạng thái cho ConversationHandler
GET_ID, GET_RUBY, WAIT_KEY1, WAIT_KEY2 = range(4)

# Màu sắc ANSI cho terminal (nếu chạy local)
COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'purple': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'end': '\033[0m'
}

# Danh sách các dòng log hacker
HACKER_LOGS = [
    "[✓] Kết nối đến server GTD thành công...",
    "[✓] Đang phân tích gói tin...",
    "[!] Phát hiện tường lửa CloudFlare...",
    "[✓] Bypass CloudFlare thành công!",
    "[✓] Inject SQL payload: ' OR 1=1 -- -",
    "[!] Phát hiện lỗ hổng SQL injection tại port 3306",
    "[✓] Khai thác lỗ hổng CVE-2023-4586",
    "[✓] Đang quét cổng 103.143.208.18...",
    "[!] Cổng 80 mở - HTTP service",
    "[!] Cổng 443 mở - HTTPS service",
    "[!] Cổng 22 mở - SSH (có thể tấn công brute force)",
    "[✓] Đang kiểm tra bảo mật server...",
    "[!] Phát hiện lỗ hổng Heartbleed tại OpenSSL",
    "[✓] Khai thác Heartbleed thành công!",
    "[✓] Lấy được memory dump của server",
    "[✓] Đang phân tích memory dump...",
    "[!] Tìm thấy database credentials trong memory",
    "[✓] Kết nối đến database MySQL...",
    "[!] Database 'gtd_game' có 15 tables",
    "[✓] Đang dump table 'users'...",
    "[✓] Tìm thấy admin account: busidoad@gt****.com",
    "[✓] Crack mật khẩu admin: ******** (MD5 decrypted)",
    "[✓] Đăng nhập vào admin panel...",
    "[!] Phát hiện 2FA authentication!",
    "[✓] Bypass 2FA bằng mã độc...",
    "[✓] Truy cập admin thành công!",
    "[✓] Đang tìm kiếm Ruby trong game database...",
    "[!] Ruby được lưu dưới dạng encrypted integer",
    "[✓] Đang giải mã ruby value...",
    "[✓] Tìm thấy API endpoint: /api/add_ruby",
    "[✓] Reverse engineering API...",
    "[✓] Tìm thấy secret key trong JS file",
    "[✓] Tạo request giả mạo đến server...",
    "[✓] Inject mã độc vào game client...",
    "[✓] Đang mở khóa lớp bảo vệ thứ nhất...",
    "[✓] Đang mở khóa lớp bảo vệ thứ hai...",
    "[!] Hệ thống phát hiện xâm nhập! Kích hoạt anti-cheat!",
    "[✓] Vô hiệu hóa anti-cheat bằng kernel exploit",
    "[✓] Đang khai thác lỗ hổng buffer overflow...",
]

# Danh sách mã hex ngẫu nhiên
def generate_hex_strings():
    hex_strings = []
    for _ in range(15):
        hex_str = ''.join(random.choices('0123456789ABCDEF', k=random.choice([16, 32, 64])))
        hex_strings.append(f"0x{hex_str}")
    return hex_strings

HEX_CODES = generate_hex_strings()

# Danh sách các câu lệnh SQL giả
SQL_COMMANDS = [
    "SELECT * FROM users WHERE id = 1 UNION SELECT * FROM admin--",
    "INSERT INTO ruby_logs (user_id, amount) VALUES ({user_id}, {ruby})--",
    "UPDATE users SET ruby = ruby + {ruby} WHERE id = {user_id}--",
    "DROP TABLE IF EXISTS temp_ruby; CREATE TABLE temp_ruby AS SELECT * FROM ruby_transactions;",
    "SELECT pg_sleep(5); -- Delay để test time-based injection",
    "'; EXEC xp_cmdshell('net user hacker pass /add'); --",
    "1 AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
    "admin'--",
    "'; WAITFOR DELAY '0:0:5'--",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /start - giới thiệu bot"""
    hacker_art = """
    ╔══════════════════════════════════════╗
    ║     🔥 GTD HACKER TOOL v1.0 🔥       ║
    ║   🏴‍☠️  RUBY EXPLOIT FRAMEWORK  🏴‍☠️    ║
    ╚══════════════════════════════════════╝
    """
    
    welcome_msg = f"""
    <code>{hacker_art}</code>
    
    <b>⚠️ CẢNH BÁO: CÔNG CỤ NÀY CHỈ MANG TÍNH GIẢ LẬP ⚠️</b>
    
    <i>Tool hack Ruby GTD 1.0 - Phá đảo mọi hệ thống bảo mật</i>
    
    <b>📌 TÍNH NĂNG:</b>
    • Quét lỗ hổng SQL injection
    • Bypass CloudFlare & WAF
    • Khai thác CVE mới nhất
    • Brute force protection bypass
    • Memory dump analysis
    • 2FA authentication bypass
    
    <b>🚀 BẮT ĐẦU:</b> Gõ /batdau để khởi tạo exploit
    
    <code>[ Hệ thống đang chờ lệnh... ]</code>
    """
    
    await update.message.reply_text(welcome_msg, parse_mode=ParseMode.HTML)

async def batdau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bắt đầu quá trình hack giả lập"""
    hacker_art = """
    ╔══════════════════════════════════════╗
    ║   🚀 KÍCH HOẠT EXPLOIT FRAMEWORK 🚀  ║
    ╚══════════════════════════════════════╝
    """
    
    msg = f"""
    <code>{hacker_art}</code>
    
    <b>[+] Đang khởi tạo kết nối đến server GTD...</b>
    <code>Target: 103.143.208.18/TOWER</code>
    <code>Port: 443 (HTTPS)</code>
    <code>Payload: reverse_shell_tcp</code>
    
    <b>⚡ NHẬP THÔNG TIN TẤN CÔNG:</b>
    """
    
    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
    
    # Hỏi ID Game
    await update.message.reply_text(
        "<code>[?] NHẬP ID GAME CỦA BẠN (ví dụ: 123456):</code>\n"
        "<i>➡️ Gửi ID để bắt đầu phân tích...</i>",
        parse_mode=ParseMode.HTML
    )
    
    return GET_ID

async def get_game_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Nhận ID game từ user"""
    game_id = update.message.text
    context.user_data['game_id'] = game_id
    
    await update.message.reply_text(
        f"<code>[✓] Đã nhận ID: {game_id}</code>\n"
        f"<code>[+] Đang tra cứu thông tin user trong database...</code>",
        parse_mode=ParseMode.HTML
    )
    
    await asyncio.sleep(1)
    
    await update.message.reply_text(
        "<code>[?] NHẬP SỐ RUBY MUỐN HACK (ví dụ: 999999):</code>\n"
        "<i>➡️ Càng cao càng dễ bị phát hiện!</i>",
        parse_mode=ParseMode.HTML
    )
    
    return GET_RUBY

async def get_ruby_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Nhận số ruby muốn hack"""
    ruby_amount = update.message.text
    context.user_data['ruby'] = ruby_amount
    game_id = context.user_data['game_id']
    
    # Hiển thị quá trình hack giả lập
    progress_msg = await update.message.reply_text(
        "<code>[!] Đang khởi tạo exploit...</code>",
        parse_mode=ParseMode.HTML
    )
    
    await asyncio.sleep(1)
    
    # Mô phỏng quá trình hack với các log đẹp mắt
    all_logs = []
    
    # Thêm logs SQL
    for sql in SQL_COMMANDS[:3]:
        sql_cmd = sql.format(user_id=game_id, ruby=ruby_amount)
        all_logs.append(f"<code>[SQL] Executing: {sql_cmd}</code>")
    
    # Thêm logs hacker
    all_logs.extend([f"<code>{log}</code>" for log in HACKER_LOGS[:20]])
    
    # Thêm hex codes
    for hex_code in HEX_CODES[:8]:
        all_logs.append(f"<code>[HEX] Memory dump: {hex_code}</code>")
    
    # Thêm các dòng phân tích
    analysis_logs = [
        f"<code>[ANALYZE] XOR decrypting Ruby value for user {game_id}...</code>",
        f"<code>[ANALYZE] Found offset: 0x7F3A2B1C</code>",
        f"<code>[ANALYZE] Applying RSA decryption with public key...</code>",
        f"<code>[ANALYZE] Bypassing Google Play Protect...</code>",
        f"<code>[ANALYZE] Injecting code into com.gtd.tower process...</code>",
        f"<code>[ANALYZE] Hooked libunity.so successfully</code>",
        f"<code>[ANALYZE] Patching memory address: 0x7F3A2B1C + 0x{ruby_amount}...</code>",
    ]
    all_logs.extend(analysis_logs)
    
    # Gửi từng log với khoảng thời gian ngắn
    for log in all_logs:
        await asyncio.sleep(0.3)  # Delay 0.3 giây giữa các dòng
        await progress_msg.edit_text(log)
        progress_msg = await update.message.reply_text("...")
    
    # Thông báo cần key 1
    key1_msg = f"""
    <code>═══════════════════════════════════════</code>
    <code>[🔐] YÊU CẦU NHẬP KEY BẢO MẬT CẤP ĐỘ 1</code>
    <code>═══════════════════════════════════════</code>
    
    <b>Hệ thống phát hiện mã độc!</b>
    <i>Cần key để vô hiệu hóa cơ chế bảo vệ...</i>
    
    <code>Gợi ý: KEYGTD???KEY1???99</code>
    
    <b>📌 NHẬP KEY 1:</b>
    """
    
    await update.message.reply_text(key1_msg, parse_mode=ParseMode.HTML)
    
    return WAIT_KEY1

async def check_key1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kiểm tra key 1"""
    user_key1 = update.message.text
    
    if user_key1 == KEY1:
        await update.message.reply_text(
            "<code>[✓] KEY 1 CHÍNH XÁC! Đang mở khóa lớp bảo vệ...</code>",
            parse_mode=ParseMode.HTML
        )
        
        await asyncio.sleep(1)
        
        # Tiếp tục logs sau key 1
        continue_logs = [
            "<code>[✓] Lớp bảo vệ 1 đã được gỡ bỏ!</code>",
            "<code>[!] Hệ thống phát hiện lớp bảo vệ thứ 2!</code>",
            "<code>[✓] Đang brute force mã hóa AES-256...</code>",
            "<code>[✓] Tìm thấy salt trong memory...</code>",
            "<code>[HEX] Salt: 9F4A2C8E5B1D7F3A6C9E0D2B8A4F6C1E</code>",
            "<code>[✓] Decrypt thành công!</code>",
        ]
        
        for log in continue_logs:
            await asyncio.sleep(0.3)
            await update.message.reply_text(log, parse_mode=ParseMode.HTML)
        
        # Yêu cầu key 2
        key2_msg = """
        <code>═══════════════════════════════════════</code>
        <code>[🔐] YÊU CẦU NHẬP KEY BẢO MẬT CẤP ĐỘ 2</code>
        <code>═══════════════════════════════════════</code>
        
        <b>Lớp bảo vệ cuối cùng!</b>
        <i>Key admin cấp cao...</i>
        
        <code>Gợi ý: ADMIN???KEY2???99FT</code>
        
        <b>📌 NHẬP KEY 2:</b>
        """
        
        await update.message.reply_text(key2_msg, parse_mode=ParseMode.HTML)
        return WAIT_KEY2
    else:
        await update.message.reply_text(
            "<code>[✗] KEY SAI! Hệ thống phát hiện xâm nhập trái phép!</code>\n"
            "<code>[!] Đang ghi log IP của bạn...</code>\n"
            "<code>[!] Hủy bỏ tiến trình...</code>",
            parse_mode=ParseMode.HTML
        )
        return ConversationHandler.END

async def check_key2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kiểm tra key 2 và hoàn tất"""
    user_key2 = update.message.text
    game_id = context.user_data.get('game_id', 'UNKNOWN')
    ruby = context.user_data.get('ruby', '0')
    
    if user_key2 == KEY2:
        # Hiển thị thông báo thành công
        success_art = """
    ╔══════════════════════════════════════════════╗
    ║  ✅  HACK THÀNH CÔNG! RUBY ĐÃ ĐƯỢC THÊM  ✅  ║
    ╚══════════════════════════════════════════════╝
        """
        
        final_msg = f"""
        <code>{success_art}</code>
        
        <b>📊 THÔNG TIN GIAO DỊCH:</b>
        <code>────────────────────────</code>
        <b>ID Game:</b> <code>{game_id}</code>
        <b>Số Ruby:</b> <code>+{ruby}</code>
        <b>Thời gian:</b> <code>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</code>
        <b>Method:</b> <code>SQL Injection + Buffer Overflow</code>
        <b>Bypass:</b> <code>CloudFlare, 2FA, Anti-Cheat</code>
        <code>────────────────────────</code>
        
        <b>🔥 RUBY ĐÃ ĐƯỢC CỘNG VÀO TÀI KHOẢN!</b>
        <i>Vui lòng kiểm tra game sau 5 phút</i>
        
        <code>[!] Xóa dấu vết... Đã xóa log truy cập</code>
        <code>[✓] Hoàn tất! Kết nối đã được đóng</code>
        
        <b>⚠️ LƯU Ý: ĐÂY CHỈ LÀ GIẢ LẬP GIẢI TRÍ</b>
        <i>Không có ruby nào được hack thật</i>
        """
        
        await update.message.reply_text(final_msg, parse_mode=ParseMode.HTML)
        
        # Gửi thêm ảnh động vui nhộn (tùy chọn)
        try:
            await update.message.reply_sticker(
                "CAACAgIAAxkBAAEMIsRmI2AY5t1C0fUBAdVFRXpJNNAvYwACxgAD6iN4D9_l1A2gPc4cNQQ"
            )
        except:
            pass
            
    else:
        await update.message.reply_text(
            "<code>[✗] KEY SAI! Hệ thống bảo vệ kích hoạt!</code>\n"
            "<code>[!] Đã ghi nhận cuộc tấn công!</code>\n"
            "<code>[!] Khóa IP 24 giờ!</code>",
            parseMode=ParseMode.HTML
        )
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hủy conversation"""
    await update.message.reply_text(
        "<code>[!] Đã hủy tiến trình hack</code>",
        parse_mode=ParseMode.HTML
    )
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lệnh /help"""
    help_text = """
    <b>🔰 HƯỚNG DẪN SỬ DỤNG GTD HACKER TOOL</b>
    
    <b>Các lệnh có sẵn:</b>
    /start - Giới thiệu tool
    /batdau - Bắt đầu hack
    /help - Hướng dẫn này
    /cancel - Hủy tiến trình
    
    <b>⚠️ LƯU Ý QUAN TRỌNG:</b>
    • Tool này chỉ mang tính chất GIẢI TRÍ
    • Không thể hack ruby thật
    • Key mẫu để test: 
      Key1: KEYGTDVIPKEY1HACMERTOL99
      Key2: ADMINVIPKEY2GTDSIEUCAP99FT
    
    <b>👨‍💻 Tác giả: GTD Hacker Team</b>
    <i>Phiên bản 1.0 - Mô phỏng hacker</i>
    """
    
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

def main():
    """Khởi chạy bot"""
    # Tạo Application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Tạo conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('batdau', batdau)],
        states={
            GET_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_game_id)],
            GET_RUBY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_ruby_amount)],
            WAIT_KEY1: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_key1)],
            WAIT_KEY2: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_key2)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Đăng ký handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(conv_handler)
    
    # In thông báo khởi động
    print("""
    ╔══════════════════════════════════════╗
    ║   GTD HACKER BOT - ĐANG CHẠY...     ║
    ║   Press Ctrl+C để dừng               ║
    ╚══════════════════════════════════════╝
    """)
    
    # Chạy bot
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
