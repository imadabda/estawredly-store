<?php
require_once 'api/db_connect.php';

$message = '';
$token_valid = false;
$token = $_GET['token'] ?? '';

if (!empty($token)) {
    // التحقق من صلاحية التوكن
    $stmt = $pdo->prepare("SELECT id FROM users WHERE reset_token = ? AND reset_expires > NOW()");
    $stmt->execute([$token]);
    if ($stmt->rowCount() > 0) {
        $token_valid = true;
    } else {
        $message = "الرابط غير صالح أو منتهي الصلاحية.";
    }
}

// معالجة تغيير كلمة المرور
if ($_SERVER['REQUEST_METHOD'] === 'POST' && $token_valid) {
    $password = $_POST['password'] ?? '';
    if (strlen($password) < 8) {
        $message = "يجب أن تتكون كلمة المرور من 8 أحرف على الأقل.";
    } else {
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);
        $update_stmt = $pdo->prepare("UPDATE users SET password = ?, reset_token = NULL, reset_expires = NULL WHERE reset_token = ?");
        if ($update_stmt->execute([$hashed_password, $token])) {
            $message = "تم تغيير كلمة المرور بنجاح. يمكنك الآن تسجيل الدخول.";
            $token_valid = false; // لإخفاء النموذج
        } else {
            $message = "حدث خطأ أثناء تغيير كلمة المرور.";
        }
    }
}
?>
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تعيين كلمة مرور جديدة | استوردلي</title>
    <style>
        body { font-family: 'Tajawal', sans-serif; background: #f8f9fa; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .reset-box { background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); width: 100%; max-width: 400px; text-align: center; }
        h2 { margin-top: 0; color: #333; }
        input[type="password"] { width: 100%; padding: 12px; margin: 15px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
        button { background: #3b82f6; color: #fff; border: none; padding: 12px; width: 100%; border-radius: 8px; font-size: 16px; cursor: pointer; }
        button:hover { background: #2563eb; }
        .message { margin-bottom: 15px; color: #d97706; font-weight: bold; }
        .success-message { color: #16a34a; }
    </style>
</head>
<body>
    <div class="reset-box">
        <h2>تعيين كلمة مرور جديدة</h2>
        <?php if (!empty($message)): ?>
            <p class="message <?php echo strpos($message, 'بنجاح') !== false ? 'success-message' : ''; ?>"><?php echo htmlspecialchars($message); ?></p>
        <?php endif; ?>

        <?php if ($token_valid): ?>
        <form method="POST">
            <input type="password" name="password" placeholder="أدخل كلمة المرور الجديدة" required>
            <button type="submit">حفظ كلمة المرور</button>
        </form>
        <?php elseif(strpos($message, 'بنجاح') !== false): ?>
            <a href="index.html" style="display:inline-block; margin-top:15px; color:#3b82f6; text-decoration:none;">العودة للصفحة الرئيسية</a>
        <?php endif; ?>
    </div>
</body>
</html>
