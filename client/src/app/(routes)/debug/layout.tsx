export default function DebugLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <main className={`mx-auto w-4/6 antialiased`}>{children}</main>;
}
