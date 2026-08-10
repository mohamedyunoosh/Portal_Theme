frappe.ui.form.on("Font", {
    refresh(frm) { update_preview(frm); },
    google_font_name(frm) { update_preview(frm); },
    css_stack(frm) { update_preview(frm); },
    font_name(frm) { update_preview(frm); },
    font_type(frm) { update_preview(frm); }
});

function update_preview(frm) {
    const stack = (frm.doc.css_stack || "").replace(/;/g, "").trim();
    const gname = (frm.doc.google_font_name || "").trim();
    const type  = frm.doc.font_type;

    if (!stack) {
        frm.fields_dict["preview_text"].$wrapper.html(
            `<div style="padding:12px;color:#888;font-size:13px">
                Enter a CSS Font Stack to see preview
            </div>`
        );
        return;
    }

    // Load Google Font
    if (type === "Google Font") {
        const fontToLoad = gname || (() => {
            const m = stack.match(/['"]([^'"]+)['"]/);
            return m ? m[1] : null;
        })();

        if (fontToLoad) {
            const id = `gf-${fontToLoad.replace(/\s+/g, "-").toLowerCase()}`;
            if (!document.getElementById(id)) {
                const link = document.createElement("link");
                link.id   = id;
                link.rel  = "stylesheet";
                link.href = `https://fonts.googleapis.com/css2?family=${encodeURIComponent(fontToLoad)}:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900&display=swap`;
                document.head.appendChild(link);
            }
        }
    }

    const preview_text = frm.doc.font_name
        ? `${frm.doc.font_name} — The quick brown fox jumps over the lazy dog`
        : "The quick brown fox jumps over the lazy dog";

    setTimeout(() => {
        const html = `
            <div style="font-family:${stack};font-size:22px;padding:16px 0 8px;
                color:var(--text-color,#333);border-bottom:1px solid #f0f0f0">
                ${preview_text}
            </div>
            <div style="font-family:${stack};font-size:14px;color:#888;
                padding-top:10px;line-height:1.8">
                ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>
                abcdefghijklmnopqrstuvwxyz<br>
                0123456789 !@#$%^&*()
            </div>
            <div style="margin-top:12px;display:flex;gap:16px;flex-wrap:wrap">
                ${[300,400,500,600,700].map(w => `
                    <div style="font-family:${stack};font-weight:${w};
                        font-size:14px;color:#555">
                        ${w} — Sample
                    </div>
                `).join("")}
            </div>
        `;
        frm.fields_dict["preview_text"].$wrapper.html(html);
    }, 1000);
}