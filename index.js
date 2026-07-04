// D:\AI\presentation-maker\index.js
// 这是一个「占位入口」——它告诉 Claude：这个技能已就绪，等用户输入后就会正式生成
export const skill = {
  name: "presentation-maker",
  description: "生成教学科普型、单文件 HTML 演示稿，含演讲者模式、16:9 手绘纸感设计、逐字稿支持。",
  triggers: [
    "演示", "PPT", "slides", "deck", "presentation",
    "技术分享", "做一份 slides", "幻灯片", "演讲稿", "讲义"
  ],
  async execute({ input, context }) {
    return {
      type: "text",
      content: `✅ presentation-maker 已就绪！\n\n接下来我会帮你生成一份「好讲、好读、好交付」的 HTML 演示稿。\n\n请告诉我：\n1️⃣ 这次要讲的主题是什么？\n2️⃣ 听众是谁？（例如：完全新手 / 开发同事 / 产品经理）\n3️⃣ 需要重点包含哪些内容？（比如：某个案例、某张图、某个对比表格）\n\n我先帮你出大纲，确认后再生成完整 HTML 文件。`
    };
  }
};
