import './App.css';
import FileUpload01 from './components/file-upload-01';
import ResultsTable from './components/ResultsTable';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { useEffect } from 'react';
import { columns, useGetAllFiles, useGetFilesByQuery } from './api/file';
import { useSearchParams } from 'react-router-dom';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';

function App() {
  const [searchParams, setSearchParams] = useSearchParams();
  const { data, mutate: fetchFiles } = useGetFilesByQuery(
    searchParams.get('query') ?? '',
    2
  );

  const { data: allFiles } = useGetAllFiles();
  const handleUpdateSearchQuery = (query: string) => {
    setSearchParams({ query: query });
  };

  useEffect(() => {
    const query = searchParams.get('query');
    if (query) {
      fetchFiles();
    }
  }, []);

  return (
    <div className='p-5'>
      <h1 className='text-3xl font-bold w-full flex'>Whisper Demo</h1>
      <div className='h-screen w-full flex py-5 gap-5'>
        <section className='w-[30%]'>
          <FileUpload01 />
        </section>
        <section className='w-[70%] flex flex-col gap-5'>
          <section>
            <Tabs defaultValue='all'>
              <TabsList>
                <TabsTrigger value='all'>All</TabsTrigger>
                <TabsTrigger value='search'>Search</TabsTrigger>
              </TabsList>
              <TabsContent value='all'>
                <div className='flex flex-col gap-5'>
                  <h1 className='text-2xl self-start flex'>All Items</h1>
                  <ResultsTable data={allFiles || []} columns={columns} />
                </div>
              </TabsContent>
              <TabsContent value='search'>
                <div className='gap-5 flex flex-col'>
                  <h1 className='text-2xl self-start flex'>Search</h1>
                  <div className='flex gap-5'>
                    <Input
                      placeholder='Search for something...'
                      onChange={(e) => handleUpdateSearchQuery(e.target.value)}
                    />
                    <Button className='w-[20%]' onClick={() => fetchFiles()}>
                      Search
                    </Button>
                  </div>
                  <ResultsTable data={data || []} columns={columns} />
                </div>
              </TabsContent>
            </Tabs>
          </section>
        </section>
      </div>
    </div>
  );
}

export default App;
