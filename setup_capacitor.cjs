
const { init, add } = require('@capacitor/cli');
async function setup() {
    try {
        await init('XiyueReader', 'org.novalreader.xiyue', { webDir: 'dist', force: true });
        console.log('✅ Capacitor init 成功');
        await add('android', { force: true });
        console.log('✅ Android 平台添加成功');
    } catch (e) {
        console.error('❌ 错误:', e.message);
        console.error('堆栈:', e.stack);
    }
}
setup();
