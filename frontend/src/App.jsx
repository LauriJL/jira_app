import { useState } from "react";

import NdaForm from "./components/NdaForm.jsx";
import NdaPreview from "./components/NdaPreview.jsx";
import { generateNda } from "./api.js";

const today = new Date().toISOString().slice(0, 10);

const initialValues = {
  party1_company: "",
  party1_name: "",
  party1_title: "",
  party1_notice: "",
  party2_company: "",
  party2_name: "",
  party2_title: "",
  party2_notice: "",
  purpose: "Evaluating whether to enter into a business relationship with the other party.",
  effective_date: today,
  mnda_term_years: 1,
  mnda_term_continues: false,
  confidentiality_years: 1,
  confidentiality_perpetual: false,
  governing_law: "",
  jurisdiction: "",
  modifications: "",
};

export default function App() {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    const { name, value, type, checked } = event.target;
    setValues((previous) => ({
      ...previous,
      [name]: type === "checkbox" ? checked : value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setErrors({});
    setFormError("");

    try {
      const data = await generateNda(values);
      setResult(data);
    } catch (error) {
      const fieldErrors = error.errors || {};
      setErrors(fieldErrors);
      setFormError(Object.keys(fieldErrors).length ? "" : error.message);
    } finally {
      setLoading(false);
    }
  }

  function handleDownload() {
    if (!result) {
      return;
    }
    const blob = new Blob([result.markdown], {
      type: "text/markdown;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = result.filename || "Mutual-NDA.md";
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="app">
      <header className="app__header">
        <h1>PreLegal</h1>
        <p>Create a Mutual NDA by filling in the key information below.</p>
      </header>

      <main className="app__main">
        <section className="panel">
          <h2>NDA details</h2>
          <NdaForm
            values={values}
            errors={errors}
            onChange={handleChange}
            onSubmit={handleSubmit}
            loading={loading}
            formError={formError}
          />
        </section>

        <section className="panel panel--preview">
          <h2>Preview</h2>
          <NdaPreview result={result} onDownload={handleDownload} />
        </section>
      </main>
    </div>
  );
}
