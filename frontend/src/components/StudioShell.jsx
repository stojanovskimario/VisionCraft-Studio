import { useState } from "react";

import App from "../App";
import PhotoEditor from "./PhotoEditor";


export default function StudioShell() {
    const [activeEditor, setActiveEditor] = useState("video");

    const buttonStyle = (selected) => ({
        padding: "11px 22px",
        borderRadius: 9,
        border: selected
            ? "1px solid #978aff"
            : "1px solid #454a58",
        background: selected ? "#5548b8" : "#242837",
        color: "#ffffff",
        fontWeight: 600,
        cursor: "pointer",
    });

    return (
        <>
            <nav
                style={{
                    display: "flex",
                    justifyContent: "center",
                    gap: 12,
                    padding: 20,
                    background: "#171b26",
                    borderBottom: "1px solid #383d4a",
                }}
            >
                <button
                    type="button"
                    onClick={() => setActiveEditor("video")}
                    style={buttonStyle(activeEditor === "video")}
                >
                    Video Editor
                </button>

                <button
                    type="button"
                    onClick={() => setActiveEditor("photo")}
                    style={buttonStyle(activeEditor === "photo")}
                >
                    Photo Editor
                </button>
            </nav>

            {/* Preserve the existing video editor and its state. */}
            <div
                style={{
                    display:
                        activeEditor === "video"
                            ? "block"
                            : "none",
                }}
            >
                <App />
            </div>

            {activeEditor === "photo" && (
                <PhotoEditor />
            )}
        </>
    );
}