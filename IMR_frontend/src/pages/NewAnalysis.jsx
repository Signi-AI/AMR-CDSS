import { useState } from "react";
import { useNavigate } from "react-router-dom";
import ImageUploader from "../components/imageUploader";
import MedicineSelect from "../components/MedicineSelect";
import ResultModal from "../components/ResultModal";
import { saveAnalysis } from "../service/api";

function NewAnalysis() {
    const navigate = useNavigate();
    const [image, setImage] = useState(null);
    const [medicine, setMedicine] = useState("");
    const [patientId, setPatientId] = useState("");
    const [age, setAge] = useState("");
    const [sex, setSex] = useState("");
    const [disease, setDisease] = useState("");

    const [errors, setErrors] = useState({});
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [submitError, setSubmitError] = useState("");
    const [results, setResults] = useState(null);
    const [showResultModal, setShowResultModal] = useState(false);
    const [medicineName, setMedicineName] = useState("");

    const validateForm = () => {
        const newErrors = {};

        if (!patientId.trim()) {
            newErrors.patientId = "Patient ID is required.";
        }

        if (!age) {
            newErrors.age = "Age is required.";
        } else if (Number(age) < 0) {
            newErrors.age = "Age cannot be negative.";
        }

        if (!sex) {
            newErrors.sex = "Please select the patient's sex.";
        }

        if (!disease.trim()) {
            newErrors.disease = "Disease or condition is required.";
        }

        if (!image) {
            newErrors.image = "Please upload a sample image.";
        }

        if (!medicine) {
            newErrors.medicine = "Please select a medicine.";
        }

        setErrors(newErrors);

        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (isAnalyzing) return;

        setSubmitError("");

        const isValid = validateForm();
        if (!isValid) return;

        setIsAnalyzing(true);

        try {
            const backendResult = await saveAnalysis({
                patientId: patientId.trim(),
                age: Number(age),
                sex,
                disease: disease.trim(),
                medicine_id: medicine,
                medicine_name: medicineName,
                image,
            });

            setResults(backendResult.recommendation);
            setShowResultModal(true);

        } catch (error) {
            console.error("Analysis failed:", error);
            setSubmitError(
                "Something went wrong while analyzing the sample. Please try again."
            );
        } finally {
            setIsAnalyzing(false);
        }
    };

    const handleCloseModal = () => {
        setShowResultModal(false);
        setResults(null);

        setImage(null);
        setMedicine("");
        setMedicineName("");
        setPatientId("");
        setAge("");
        setSex("");
        setDisease("");

        navigate("/history");
    };

    return (
        <div className="mx-auto max-w-5xl">

            {/* Page heading */}
            <div>
                <p className="text-sm font-medium text-teal-600">
                    SAMPLE ANALYSIS
                </p>

                <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-900">
                    New Analysis
                </h1>

                <p className="mt-2 max-w-2xl text-slate-500">
                    Provide the sample information and upload an image
                    for AI-assisted antimicrobial analysis.
                </p>
            </div>

            {/* Submit error */}
            {submitError && (
                <div className="mt-6 rounded-lg border border-red-200 bg-red-50 px-4 py-3">
                    <p className="text-sm font-medium text-red-700">
                        {submitError}
                    </p>
                </div>
            )}

            <form onSubmit={handleSubmit} className="mt-8 space-y-8">

                {/* Patient information */}
                <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">

                    <div>
                        <h2 className="text-lg font-semibold text-slate-900">
                            Patient Information
                        </h2>

                        <p className="mt-1 text-sm text-slate-500">
                            Enter the basic information associated with this sample.
                        </p>
                    </div>

                    <div className="mt-6 grid gap-5 md:grid-cols-3">

                        {/* Patient ID */}
                        <div>
                            <label
                                htmlFor="patientId"
                                className="text-sm font-medium text-slate-700"
                            >
                                Patient ID
                            </label>

                            <input
                                id="patientId"
                                type="text"
                                value={patientId}
                                onChange={(event) => {
                                    setPatientId(event.target.value);

                                    if (errors.patientId) {
                                        setErrors((previous) => ({
                                            ...previous,
                                            patientId: "",
                                        }));
                                    }
                                }}
                                placeholder="e.g. PT-001"
                                className={`mt-2 w-full rounded-lg border px-4 py-3 text-sm outline-none transition focus:ring-2 ${
                                    errors.patientId
                                        ? "border-red-400 focus:border-red-500 focus:ring-red-100"
                                        : "border-slate-300 focus:border-teal-500 focus:ring-teal-100"
                                }`}
                            />

                            {errors.patientId && (
                                <p className="mt-1 text-xs text-red-600">
                                    {errors.patientId}
                                </p>
                            )}
                        </div>

                        {/* Age */}
                        <div>
                            <label
                                htmlFor="age"
                                className="text-sm font-medium text-slate-700"
                            >
                                Age
                            </label>

                            <input
                                id="age"
                                type="number"
                                min="0"
                                value={age}
                                onChange={(event) => {
                                    setAge(event.target.value);

                                    if (errors.age) {
                                        setErrors((previous) => ({
                                            ...previous,
                                            age: "",
                                        }));
                                    }
                                }}
                                placeholder="Age"
                                className={`mt-2 w-full rounded-lg border px-4 py-3 text-sm outline-none transition focus:ring-2 ${
                                    errors.age
                                        ? "border-red-400 focus:border-red-500 focus:ring-red-100"
                                        : "border-slate-300 focus:border-teal-500 focus:ring-teal-100"
                                }`}
                            />

                            {errors.age && (
                                <p className="mt-1 text-xs text-red-600">
                                    {errors.age}
                                </p>
                            )}
                        </div>

                        {/* Sex */}
                        <div>
                            <label
                                htmlFor="sex"
                                className="text-sm font-medium text-slate-700"
                            >
                                Sex
                            </label>

                            <select
                                id="sex"
                                value={sex}
                                onChange={(event) => {
                                    setSex(event.target.value);

                                    if (errors.sex) {
                                        setErrors((previous) => ({
                                            ...previous,
                                            sex: "",
                                        }));
                                    }
                                }}
                                className={`mt-2 w-full rounded-lg border bg-white px-4 py-3 text-sm outline-none transition focus:ring-2 ${
                                    errors.sex
                                        ? "border-red-400 focus:border-red-500 focus:ring-red-100"
                                        : "border-slate-300 focus:border-teal-500 focus:ring-teal-100"
                                }`}
                            >
                                <option value="">Select sex</option>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                            </select>

                            {errors.sex && (
                                <p className="mt-1 text-xs text-red-600">
                                    {errors.sex}
                                </p>
                            )}
                        </div>

                    </div>
                </section>

                {/* Clinical information */}
                <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">

                    <div>
                        <h2 className="text-lg font-semibold text-slate-900">
                            Clinical Information
                        </h2>

                        <p className="mt-1 text-sm text-slate-500">
                            Provide the condition identified by the healthcare professional.
                        </p>
                    </div>

                    <div className="mt-6 max-w-xl">

                        <label
                            htmlFor="disease"
                            className="text-sm font-medium text-slate-700"
                        >
                            Disease / Condition
                        </label>

                        <input
                            id="disease"
                            type="text"
                            value={disease}
                            onChange={(event) => {
                                setDisease(event.target.value);

                                if (errors.disease) {
                                    setErrors((previous) => ({
                                        ...previous,
                                        disease: "",
                                    }));
                                }
                            }}
                            placeholder="e.g. urinary tract infection"
                            className={`mt-2 w-full rounded-lg border px-4 py-3 text-sm outline-none transition focus:ring-2 ${
                                errors.disease
                                    ? "border-red-400 focus:border-red-500 focus:ring-red-100"
                                    : "border-slate-300 focus:border-teal-500 focus:ring-teal-100"
                            }`}
                        />

                        {errors.disease && (
                            <p className="mt-1 text-xs text-red-600">
                                {errors.disease}
                            </p>
                        )}

                        <p className="mt-2 text-xs text-slate-400">
                            The final list of supported conditions will be determined
                            from the available clinical data and ML model.
                        </p>

                    </div>
                </section>

                {/* Sample image */}
                <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">

                    <div>
                        <h2 className="text-lg font-semibold text-slate-900">
                            Sample Image
                        </h2>

                        <p className="mt-1 text-sm text-slate-500">
                            Upload the image captured from the microscope device.
                        </p>
                    </div>

                    <ImageUploader
                        image={image}
                        onImageChange={(file) => {
                            setImage(file);

                            if (file && errors.image) {
                                setErrors((previous) => ({
                                    ...previous,
                                    image: "",
                                }));
                            }
                        }}
                    />

                    {/* Form-level image error */}
                    {errors.image && !image && (
                        <p className="mt-3 text-sm text-red-600">
                            {errors.image}
                        </p>
                    )}

                </section>

                {/* Medicine */}
                <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">

                    <div>
                        <h2 className="text-lg font-semibold text-slate-900">
                            Antimicrobial
                        </h2>

                        <p className="mt-1 text-sm text-slate-500">
                            Select the antimicrobial being considered for the patient.
                        </p>
                    </div>

                    <div className="mt-6 max-w-md">
                        <MedicineSelect
                            value={medicine}
                            onChange={(value) => {
                                setMedicine(value);

                                if (errors.medicine) {
                                    setErrors((previous) => ({
                                        ...previous,
                                        medicine: "",
                                    }));
                                }
                            }}
                            onMedicineNameChange={setMedicineName}
                            error={errors.medicine}
                        />
                    </div>
                </section>

                {/* Submit */}
                <div className="flex justify-end pb-8">

                    <button
                        type="submit"
                        disabled={isAnalyzing}
                        className={`rounded-lg px-6 py-3 text-sm font-semibold text-white shadow-sm transition focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2 ${
                            isAnalyzing
                                ? "cursor-not-allowed bg-teal-300 opacity-70"
                                : "bg-teal-500 hover:bg-teal-600"
                        }`}
                    >
                        {isAnalyzing ? (
                            <span className="flex items-center gap-2">
                <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                Analyzing...
              </span>
                        ) : (
                            "Analyze Sample"
                        )}
                    </button>

                </div>

            </form>

            {/* Result modal */}
            <ResultModal
                open={showResultModal}
                results={results}
                analysisData={{
                    patientId: patientId.trim(),
                    medicine,
                    disease: disease.trim(),
                }}
                onClose={handleCloseModal}
            />
        </div>
    );
}

export default NewAnalysis;