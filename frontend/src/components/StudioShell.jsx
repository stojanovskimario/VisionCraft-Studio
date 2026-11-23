
import { useState } from "react";

import App from "../App";
import PhotoEditor from "./PhotoEditor";

import "./StudioShell.css";
import "./StudioPalette.css";


function EditorIcon({ type }) {
    if (type === "video") {
        return (
            <svg viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" strokeWidth="1.8"
                 strokeLinecap="round" strokeLinejoin="round"
                 aria-hidden="true">
                <rect x="3" y="5" width="14" height="14" rx="3" />
                <path d="m17 10 4-3v10l-4-3" />
            </svg>
        );
    }

    return (
        <svg viewBox="0 0 24 24" fill="none"
             stroke="currentColor" strokeWidth="1.8"
             strokeLinecap="round" strokeLinejoin="round"
             aria-hidden="true">
            <rect x="3" y="3" width="18" height="18" rx="3" />
            <circle cx="8.5" cy="8.5" r="1.5" />
            <path d="m3 17 5-5 4 4 3-3 6 6" />
        </svg>
    );
}


export default function StudioShell() {
    const [activeEditor, setActiveEditor] = useState("video");

    return (
        <div className="studio-shell">
            <header className="studio-header">
                <div className="studio-header__inner">
                    <div className="studio-brand">
                        <span className="studio-brand__symbol">
                            <svg viewBox="0 0 36 36" fill="none"
                                 aria-hidden="true">
                                <rect x="3" y="3" width="30" height="30"
                                      rx="9" stroke="currentColor"
                                      strokeWidth="2" />
                                <path d="M11 24 17 11l4 9 4-6"
                                      stroke="currentColor"
                                      strokeWidth="2.5"
                                      strokeLinecap="round"
                                      strokeLinejoin="round" />
                                <circle cx="26" cy="24" r="3"
                                        fill="currentColor" />
                            </svg>
                        </span>

                        <div className="studio-brand__text">
                            <strong>VisionCraft<span>Studio</span></strong>
                            <small>CREATIVE WORKSPACE</small>
                        </div>
                    </div>

                    <nav className="studio-navigation"
                         aria-label="Editor selection">
                        <button
                            type="button"
                            className={
                                "studio-navigation__button" +
                                (activeEditor === "video"
                                    ? " studio-navigation__button--active"
                                    : "")
                            }
                            aria-pressed={activeEditor === "video"}
                            onClick={() => setActiveEditor("video")}
                        >
                            <EditorIcon type="video" />
                            <span>Video Editor</span>
                        </button>

                        <button
                            type="button"
                            className={
                                "studio-navigation__button" +
                                (activeEditor === "photo"
                                    ? " studio-navigation__button--active"
                                    : "")
                            }
                            aria-pressed={activeEditor === "photo"}
                            onClick={() => setActiveEditor("photo")}
                        >
                            <EditorIcon type="photo" />
                            <span>Photo Editor</span>
                        </button>
                    </nav>
                </div>
            </header>

            <div
                className="studio-shell__video"
                style={{
                    display: activeEditor === "video"
                        ? "block"
                        : "none",
                }}
            >
                <App />
            </div>

            <div
                className="studio-shell__photo"
                style={{
                    display: activeEditor === "photo"
                        ? "block"
                        : "none",
                }}
            >
                <PhotoEditor />
            </div>
        </div>
    );
}
