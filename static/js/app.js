const form = document.getElementById("predictForm");
const resultCard = document.getElementById("resultCard");
const resultContent = document.getElementById("resultContent");
const submitBtn = document.getElementById("submitBtn");
const fillSampleBtn = document.getElementById("fillSample");


const SAMPLE_DATA = {
    product_quality: "M",
    air_temperature: "298.1",
    process_temperature: "308.6",
    rotational_speed: "1551",
    torque: "42.8",
    tool_wear: "0",
};

const VALID_PRODUCT_QUALITIES = ["L", "M", "H"];
const NUMERIC_FIELDS = [
    "air_temperature",
    "process_temperature",
    "rotational_speed",
    "torque",
    "tool_wear",
];

function setFieldValue(id, value) {
    const el = document.getElementById(id);
    if (!el) return;

    const stringValue = String(value);
    if (el.tagName === "SELECT") {
        const hasOption = Array.from(el.options).some((opt) => opt.value === stringValue);
        if (!hasOption) return;
    }

    el.value = stringValue;
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
}

fillSampleBtn.addEventListener("click", () => {
    for (const [key, value] of Object.entries(SAMPLE_DATA)) {
        setFieldValue(key, value);
    }
    resultCard.classList.add("hidden");
});

function readFormPayload() {
    return {
        product_quality: document.getElementById("product_quality").value.trim(),
        air_temperature: parseFloat(document.getElementById("air_temperature").value),
        process_temperature: parseFloat(document.getElementById("process_temperature").value),
        rotational_speed: parseFloat(document.getElementById("rotational_speed").value),
        torque: parseFloat(document.getElementById("torque").value),
        tool_wear: parseFloat(document.getElementById("tool_wear").value),
    };
}

function validatePayload(payload) {
    if (!VALID_PRODUCT_QUALITIES.includes(payload.product_quality)) {
        return "Lütfen ürün kalitesini (L, M veya H) seçin.";
    }

    if (NUMERIC_FIELDS.some((key) => Number.isNaN(payload[key]))) {
        return "Lütfen tüm sensör alanlarını geçerli sayılarla doldurun.";
    }

    return null;
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = readFormPayload();
    const validationError = validatePayload(payload);
    if (validationError) {
        showError(validationError);
        return;
    }

    setLoading(true);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            const detail = err.detail;
            let message = "Tahmin isteği başarısız oldu.";

            if (typeof detail === "string") {
                message = detail;
            } else if (Array.isArray(detail) && detail.length > 0) {
                message = detail.map((item) => item.msg).join(" ");
            }

            throw new Error(message);
        }

        const data = await response.json();
        showResult(data);
    } catch (err) {
        showError(err.message || "Bir hata oluştu. Sunucunun çalıştığından emin olun.");
    } finally {
        setLoading(false);
    }
});

function setLoading(loading) {
    submitBtn.disabled = loading;
    submitBtn.querySelector(".btn-text").textContent = loading ? "Tahmin ediliyor..." : "Tahmin Et";
    submitBtn.querySelector(".spinner").classList.toggle("hidden", !loading);
}

function showError(message) {
    resultCard.classList.remove("hidden");
    resultContent.innerHTML = `<div class="error-msg">${escapeHtml(message)}</div>`;
}

function showResult(data) {
    const isNoFailure = data.predicted_class === "No Failure";
    const sorted = [...data.probabilities].sort((a, b) => b.probability - a.probability);

    resultContent.innerHTML = `
        <div class="prediction-main ${isNoFailure ? "no-failure" : "failure"}">
            <div>
                <div class="prediction-label">${escapeHtml(data.predicted_class)}</div>
                <div class="prediction-confidence">Güven: %${data.confidence}</div>
            </div>
        </div>
        <div class="probabilities">
            <h4>Sınıf Olasılıkları</h4>
            ${sorted.map((p) => `
                <div class="prob-row">
                    <span class="prob-label" title="${escapeHtml(p.label)}">${escapeHtml(p.label)}</span>
                    <div class="prob-bar-wrap">
                        <div class="prob-bar" style="width: ${p.probability}%"></div>
                    </div>
                    <span class="prob-value">%${p.probability}</span>
                </div>
            `).join("")}
        </div>
    `;

    resultCard.classList.remove("hidden");
    resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
