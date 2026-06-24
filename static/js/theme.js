document.addEventListener(
    "DOMContentLoaded",
    function ()
    {
        const toggle =
            document.getElementById(
                "theme-toggle"
            );

        const savedTheme =
            localStorage.getItem(
                "theme"
            );

        if (savedTheme === "dark")
        {
            document.body.classList.add(
                "dark-mode"
            );

            if (toggle)
            {
                toggle.checked = true;
            }
        }

        if (toggle)
        {
            toggle.addEventListener(
                "change",
                function ()
                {
                    if (this.checked)
                    {
                        document.body.classList.add(
                            "dark-mode"
                        );

                        localStorage.setItem(
                            "theme",
                            "dark"
                        );
                    }
                    else
                    {
                        document.body.classList.remove(
                            "dark-mode"
                        );

                        localStorage.setItem(
                            "theme",
                            "light"
                        );
                    }
                }
            );
        }
    }
);