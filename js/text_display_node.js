import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

app.registerExtension({
    name: "org.example.TextDisplay",
    nodeType: "TextDisplay",
    nodeData: {
        "name": "TextDisplay",
        "display_name": "Display Text",
        "category": "utils",
        "description": "Displays input text",
        "input": {
            "text": ["STRING", {"multiline": true}]
        },
        "output": null
    },
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function() {
            if (onNodeCreated) {
                onNodeCreated.apply(this, arguments);
            }
            this.textWidget = null;
        };

        const onExecuted = function(message) {
            if (message && message.text !== undefined) {
                const text = Array.isArray(message.text) ? message.text.join('') : message.text;
                if (!this.textWidget) {
                    // 动态创建 textarea widget
                    this.textWidget = ComfyWidgets["STRING"](this, "", ["STRING", { multiline: true }], app).widget;
                    this.textWidget.inputEl.style.fontSize = "12px";
                    this.textWidget.inputEl.style.height = "100%";
                    this.textWidget.inputEl.style.width = "100%";
                    this.textWidget.inputEl.style.backgroundColor = "#2a2a2a";
                    this.textWidget.inputEl.style.color = "#ffffff";
                    this.textWidget.inputEl.readOnly = true;
                    this.textWidget.inputEl.style.overflowY = "auto";
                }
                this.textWidget.value = text;
                this.textWidget.inputEl.value = text;
                this.setSize([350, 200]);
            }
            this.setDirtyCanvas(true);
        };

        Object.assign(nodeType.prototype, {
            onExecuted
        });
    },
});