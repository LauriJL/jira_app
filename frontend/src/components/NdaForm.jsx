function Field({ label, name, error, hint, children }) {
  return (
    <label className="field">
      <span className="field__label">{label}</span>
      {children}
      {hint && !error ? <span className="field__hint">{hint}</span> : null}
      {error ? <span className="field__error">{error}</span> : null}
    </label>
  );
}

export default function NdaForm({ values, errors, onChange, onSubmit, loading, formError }) {
  return (
    <form className="form" onSubmit={onSubmit} noValidate>
      <fieldset>
        <legend>Party 1</legend>
        <Field label="Company" name="party1_company" error={errors.party1_company}>
          <input
            type="text"
            name="party1_company"
            value={values.party1_company}
            onChange={onChange}
            placeholder="Acme Corp"
          />
        </Field>
        <Field label="Print name" name="party1_name" error={errors.party1_name}>
          <input type="text" name="party1_name" value={values.party1_name} onChange={onChange} />
        </Field>
        <Field label="Title" name="party1_title" error={errors.party1_title}>
          <input type="text" name="party1_title" value={values.party1_title} onChange={onChange} />
        </Field>
        <Field
          label="Notice address"
          name="party1_notice"
          error={errors.party1_notice}
          hint="Email or postal address"
        >
          <input type="text" name="party1_notice" value={values.party1_notice} onChange={onChange} />
        </Field>
      </fieldset>

      <fieldset>
        <legend>Party 2</legend>
        <Field label="Company" name="party2_company" error={errors.party2_company}>
          <input
            type="text"
            name="party2_company"
            value={values.party2_company}
            onChange={onChange}
            placeholder="Globex LLC"
          />
        </Field>
        <Field label="Print name" name="party2_name" error={errors.party2_name}>
          <input type="text" name="party2_name" value={values.party2_name} onChange={onChange} />
        </Field>
        <Field label="Title" name="party2_title" error={errors.party2_title}>
          <input type="text" name="party2_title" value={values.party2_title} onChange={onChange} />
        </Field>
        <Field
          label="Notice address"
          name="party2_notice"
          error={errors.party2_notice}
          hint="Email or postal address"
        >
          <input type="text" name="party2_notice" value={values.party2_notice} onChange={onChange} />
        </Field>
      </fieldset>

      <fieldset>
        <legend>Agreement terms</legend>
        <Field label="Purpose" name="purpose" error={errors.purpose}>
          <textarea name="purpose" rows="2" value={values.purpose} onChange={onChange} />
        </Field>

        <Field label="Effective date" name="effective_date" error={errors.effective_date}>
          <input
            type="date"
            name="effective_date"
            value={values.effective_date}
            onChange={onChange}
          />
        </Field>

        <Field label="MNDA term" name="mnda_term_years" error={errors.mnda_term_years}>
          <div className="choice">
            <label className="choice__option">
              <input
                type="radio"
                name="mnda_term_continues"
                checked={!values.mnda_term_continues}
                onChange={() => onChange({ target: { name: "mnda_term_continues", type: "checkbox", checked: false } })}
              />
              Expires after
            </label>
            <input
              className="choice__number"
              type="number"
              min="1"
              name="mnda_term_years"
              value={values.mnda_term_years}
              onChange={onChange}
              disabled={values.mnda_term_continues}
            />
            <span>year(s) from the Effective Date</span>
          </div>
          <div className="choice">
            <label className="choice__option">
              <input
                type="radio"
                name="mnda_term_continues"
                checked={values.mnda_term_continues}
                onChange={() => onChange({ target: { name: "mnda_term_continues", type: "checkbox", checked: true } })}
              />
              Continues until terminated
            </label>
          </div>
        </Field>

        <Field
          label="Term of confidentiality"
          name="confidentiality_years"
          error={errors.confidentiality_years}
        >
          <div className="choice">
            <label className="choice__option">
              <input
                type="radio"
                name="confidentiality_perpetual"
                checked={!values.confidentiality_perpetual}
                onChange={() => onChange({ target: { name: "confidentiality_perpetual", type: "checkbox", checked: false } })}
              />
              Protected for
            </label>
            <input
              className="choice__number"
              type="number"
              min="1"
              name="confidentiality_years"
              value={values.confidentiality_years}
              onChange={onChange}
              disabled={values.confidentiality_perpetual}
            />
            <span>year(s) from the Effective Date</span>
          </div>
          <div className="choice">
            <label className="choice__option">
              <input
                type="radio"
                name="confidentiality_perpetual"
                checked={values.confidentiality_perpetual}
                onChange={() => onChange({ target: { name: "confidentiality_perpetual", type: "checkbox", checked: true } })}
              />
              In perpetuity
            </label>
          </div>
        </Field>

        <Field label="Governing law" name="governing_law" error={errors.governing_law}>
          <input
            type="text"
            name="governing_law"
            value={values.governing_law}
            onChange={onChange}
            placeholder="Delaware"
          />
        </Field>

        <Field
          label="Jurisdiction"
          name="jurisdiction"
          error={errors.jurisdiction}
          hint="City or county and state, e.g. New Castle, DE"
        >
          <input
            type="text"
            name="jurisdiction"
            value={values.jurisdiction}
            onChange={onChange}
            placeholder="New Castle, DE"
          />
        </Field>

        <Field label="Modifications (optional)" name="modifications" error={errors.modifications}>
          <textarea name="modifications" rows="2" value={values.modifications} onChange={onChange} />
        </Field>
      </fieldset>

      {formError ? <p className="form__error">{formError}</p> : null}

      <button type="submit" className="button" disabled={loading}>
        {loading ? "Generating\u2026" : "Generate NDA"}
      </button>
    </form>
  );
}
