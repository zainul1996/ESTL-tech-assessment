module.exports = {
    darkMode: 'class',
    theme: {
        extend: {
            screens: {
                dark: { raw: '(prefers-color-scheme: light)' }
            },
            width: {
                '76': 'calc(100% - 18rem)',
            },
        }
    }
}