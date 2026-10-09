import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function NdaPreview({ result, onDownload }) {
  if (!result) {
    return (
      <div className="preview preview--empty">
        <p>Fill in the form and generate the NDA to see a preview here.</p>
      </div>
    );
  }

  return (
    <div className="preview">
      <div className="preview__toolbar">
        <button type="button" className="button button--secondary" onClick={onDownload}>
          Download .md
        </button>
      </div>
      <article className="preview__document">
        <Markdown remarkPlugins={[remarkGfm]}>{result.markdown}</Markdown>
      </article>
    </div>
  );
}
