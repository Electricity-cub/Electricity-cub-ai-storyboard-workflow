#!/bin/bash

# AI分镜师工作流快速测试脚本

echo "========================================="
echo "   AI分镜师工作流 - 快速测试"
echo "========================================="
echo ""

# 检查服务是否运行
echo "🔍 检查服务状态..."
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ 服务已在运行"
else
    echo "❌ 服务未运行，正在启动..."
    echo ""
    echo "⚠️  请在另一个终端窗口执行："
    echo "   bash scripts/http_run.sh -p 5000"
    echo ""
    echo "等待服务启动后，再运行此脚本"
    exit 1
fi

echo ""

# 创建测试输入
echo "📝 准备测试输入..."
cat > test_input.json << 'EOF'
{
  "script_content": "第1集：荒海求生\n\n【场景：甲板 - 日】\n\nP01：苏醒\n\n海面上空，一艘破旧的货船在灰蓝阴天下漂浮。\n\n甲板上，凌羽慢慢睁开眼睛，发现自己躺在横七竖八的女生中间。女生们面色苍白，长发凌乱，一动不动。\n\n凌羽（惊恐）：这是哪儿？\n\n洛凝雪（虚弱）：我们...好像在海上。\n\n凌羽站起身，环顾四周。桅杆断裂，残帆在风中抖动。船舱紧闭，看不出任何生机。",
  "episode_number": "ep01",
  "visual_style": "写实",
  "project_type": "国内短剧",
  "target_language": null
}
EOF

echo "✅ 测试输入已创建"

# 调用API
echo ""
echo "🚀 调用工作流API..."
echo ""

START_TIME=$(date +%s)

curl -X POST http://localhost:5000/api/v1/run \
  -H "Content-Type: application/json" \
  -d @test_input.json \
  -o test_output.json

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 工作流执行成功！"
    echo "⏱️  耗时: ${DURATION}秒"
    echo ""
    echo "📊 输出文件: test_output.json"
    echo ""
    echo "📋 输出内容预览:"
    echo "----------------------------------------"
    cat test_output.json | head -n 50
    echo "----------------------------------------"
    echo ""
    echo "💡 查看完整输出: cat test_output.json"
    echo "💡 格式化查看: cat test_output.json | jq ."
else
    echo ""
    echo "❌ 工作流执行失败"
    echo "请检查日志: cat /app/work/logs/bypass/app.log"
fi
