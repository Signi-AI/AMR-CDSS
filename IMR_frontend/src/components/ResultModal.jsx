
function ResultModal({ open, results, analysisData, onClose }) {
    if (!open) {
        return null;
    }

    const isGood = results.adverseReactionRisk === "Low";

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4">
            <div className="max-h-[90vh] w-full max-w-xl overflow-y-auto rounded-2xl bg-white p-6 shadow-xl">
                {/* Header */}
                <div className="text-center">
                    <p className="text-sm font-medium text-teal-600">
                        ANALYSIS COMPLETE
                    </p>

                    <h2 className="mt-2 text-2xl font-bold text-slate-900">
                        AI Analysis Result
                    </h2>
                </div>

                {/* Single AI answer */}
                <div
                    className={`mt-6 rounded-xl border p-5 ${
                        isGood
                            ? "border-teal-200 bg-teal-50/60"
                            : "border-red-200 bg-red-50/60"
                    }`}
                >
                    <div className="flex items-center justify-between gap-3">
                        <p className="text-sm font-semibold text-slate-700">
                            Recommendation
                        </p>

                        <span
                            className={`shrink-0 rounded-full px-3 py-1 text-xs font-bold ${
                                isGood
                                    ? "bg-teal-100 text-teal-700"
                                    : "bg-red-100 text-red-600"
                            }`}
                        >
                            {results.adverseReactionRisk} Risk
                        </span>
                    </div>

                    <p className="mt-3 text-sm leading-relaxed text-slate-700">
                        {results.message}
                    </p>
                </div>

                {/* Details */}
                <div className="mt-6 rounded-xl border border-slate-200 bg-slate-50 p-4">
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                        Sample details
                    </p>

                    <div className="mt-3 grid gap-3 sm:grid-cols-3">
                        <div>
                            <p className="text-xs text-slate-500">Patient ID</p>
                            <p className="mt-0.5 font-medium text-slate-900">
                                {analysisData.patientId}
                            </p>
                        </div>

                        <div>
                            <p className="text-xs text-slate-500">Medicine</p>
                            <p className="mt-0.5 font-medium text-slate-900">
                                {analysisData.medicine}
                            </p>
                        </div>

                        <div>
                            <p className="text-xs text-slate-500">Disease</p>
                            <p className="mt-0.5 font-medium text-slate-900">
                                {analysisData.disease}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Close button */}
                <button
                    type="button"
                    onClick={onClose}
                    className="mt-6 w-full rounded-lg bg-teal-500 px-6 py-3 text-sm font-semibold text-white transition hover:bg-teal-600"
                >
                    Close
                </button>
            </div>
        </div>
    );
}

export default ResultModal;