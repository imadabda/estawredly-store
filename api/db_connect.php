<?php
// ══════════════════════════════════════════════════
// ملف الاتصال بقاعدة بيانات Hostinger
// ══════════════════════════════════════════════════

// ضع بيانات قاعدة البيانات الخاصة بك هنا عندما ترفع الملفات إلى Hostinger
$db_host = 'localhost'; 
$db_user = 'root'; // استبدله باسم مستخدم قاعدة بيانات Hostinger
$db_pass = ''; // استبدله بكلمة مرور قاعدة بيانات Hostinger
$db_name = 'estawredly_db'; // استبدله باسم قاعدة بيانات Hostinger

// إعداد الترويسات (Headers) للتعامل مع الـ API
header('Content-Type: application/json; charset=utf-8');

try {
    // إنشاء الاتصال باستخدام PDO لتوفير أقصى درجات الحماية من الاختراقات (SQL Injection)
    $pdo = new PDO("mysql:host=$db_host;dbname=$db_name;charset=utf8mb4", $db_user, $db_pass);
    
    // إعداد PDO لإظهار الأخطاء بشكل واضح
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

} catch (PDOException $e) {
    // إرسال خطأ في حال فشل الاتصال
    echo json_encode([
        'success' => false,
        'message' => 'فشل الاتصال بقاعدة البيانات: ' . $e->getMessage()
    ]);
    exit;
}
?>
