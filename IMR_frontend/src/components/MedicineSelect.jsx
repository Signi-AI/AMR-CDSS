import { useState, useEffect } from "react";
import { getMedicines } from "../service/api";

function MedicineSelect({ value, onChange, error, onMedicineNameChange }) {
    const [medicines, setMedicines] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchMedicines() {
            try {
                const data = await getMedicines();
                setMedicines(data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        }
        fetchMedicines();
    }, []);

    const handleChange = (event) => {
        const val = event.target.value;
        onChange(val);
        if (onMedicineNameChange) {
            const selected = medicines.find((m) => String(m.id) === val);
            if (selected) {
                onMedicineNameChange(selected.name);
            } else {
                onMedicineNameChange("");
            }
        }
    };

    return (
        <div>
            <label
                htmlFor="medicine"
                className="text-sm font-medium text-slate-700"
            >
                Medicine
            </label>

            <select
                id="medicine"
                value={value}
                onChange={handleChange}
                disabled={loading}
                className={`mt-2 w-full rounded-lg border bg-white px-4 py-3 text-sm outline-none transition focus:ring-2 ${
                    error
                        ? "border-red-400 focus:border-red-500 focus:ring-red-100"
                        : "border-slate-300 focus:border-teal-500 focus:ring-teal-100"
                }`}
            >
                <option value="">{loading ? "Loading..." : "Select medicine"}</option>
                {medicines.map((medicine) => (
                    <option key={medicine.id} value={medicine.id}>
                        {medicine.name}
                    </option>
                ))}
            </select>

            {error && (
                <p className="mt-1 text-xs text-red-600">
                    {error}
                </p>
            )}
        </div>
    );
}

export default MedicineSelect;