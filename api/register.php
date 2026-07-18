<?php
session_start();
require_once 'db_connect.php';

// التأكد من أن الطلب من نوع POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'message' => 'طريقة طلب غير صالحة']);
    exit;
}

// قراءة البيانات القادمة من JSON (Fetch API)
$data = json_decode(file_get_contents('php://input'), true);

$name = trim($data['name'] ?? '');
$email = trim($data['email'] ?? '');
$password = $data['password'] ?? '';
$phone = trim($data['phone'] ?? '');

// التحقق من صحة المدخلات
if (empty($name) || empty($email) || empty($password)) {
    echo json_encode(['success' => false, 'message' => 'يرجى تعبئة جميع الحقول المطلوبة (الاسم، البريد، كلمة المرور)']);
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo json_encode(['success' => false, 'message' => 'البريد الإلكتروني غير صالح']);
    exit;
}

if (strlen($password) < 8) {
    echo json_encode(['success' => false, 'message' => 'يجب أن تتكون كلمة المرور من 8 أحرف على الأقل']);
    exit;
}

try {
    // التأكد من أن البريد الإلكتروني غير مستخدم مسبقاً
    $stmt = $pdo->prepare("SELECT id FROM users WHERE email = ?");
    $stmt->execute([$email]);
    if ($stmt->rowCount() > 0) {
        echo json_encode(['success' => false, 'message' => 'البريد الإلكتروني مسجل مسبقاً']);
        exit;
    }

    // تشفير كلمة المرور بقوة
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    // إدخال المستخدم في قاعدة البيانات
    $insert_stmt = $pdo->prepare("INSERT INTO users (name, email, password, phone, role) VALUES (?, ?, ?, ?, 'customer')");
    
    if ($insert_stmt->execute([$name, $email, $hashed_password, $phone])) {
        // تسجيل الدخول التلقائي بعد إنشاء الحساب
        $user_id = $pdo->lastInsertId();
        
        $_SESSION['user_id'] = $user_id;
        $_SESSION['user_name'] = $name;
        $_SESSION['user_email'] = $email;
        $_SESSION['user_role'] = 'customer';

        echo json_encode([
            'success' => true, 
            'message' => 'تم إنشاء الحساب بنجاح',
            'user' => [
                'name' => $name,
                'email' => $email,
                'role' => 'customer'
            ]
        ]);
    } else {
        echo json_encode(['success' => false, 'message' => 'حدث خطأ أثناء إنشاء الحساب، يرجى المحاولة لاحقاً']);
    }

} catch (PDOException $e) {
    echo json_encode(['success' => false, 'message' => 'خطأ في قاعدة البيانات']);
}
?>
