# Namex SOLR Implementation

## Search Core Config
- luceneMatchVersion
```
  <luceneMatchVersion>6.6.3</luceneMatchVersion>
```
Specifies the Lucene version compatibility
Critical for ensuring consistent behavior across components

- Data Directory [dataDir]
```
  <dataDir>${solr.data.dir:}</dataDir>
```
**Required: No**

Defines the location for index data storage
Uses system property substitution with fallback to default

Used to specify an alternate directory to hold all index data other than the default ./data under the Solr home.  If replication is in use, this should match the replication configuration.

Think of this like choosing where and how to store books in a library then dataDir is like choosing which building to store your books in.

### Directory Factory [directoryFactory]
```
  <directoryFactory name="DirectoryFactory"
                    class="${solr.directoryFactory:solr.NRTCachingDirectoryFactory}"/>
```

Configures how Solr manages index storage
Default: NRTCachingDirectoryFactory (is memory-based and optimized for Near Real Time searches)

Alternatives include:
  - StandardDirectoryFactory:
This is Solr's default directory factory. Think of it as a smart manager that automatically chooses the best directory implementation based on your operating system and available options. It typically selects between MMapDirectory and NIOFSDirectory, making it a safe and reliable choice for most use cases. When you start Solr without specifying a directory factory, this is what you get.
  - MMapDirectoryFactory:
This factory uses memory-mapped files (mmap) to access the index. Imagine your index files being directly mapped into your application's memory space - when you read from that memory address, you're actually reading from the file. This approach can provide excellent performance, especially for large indices, because it leverages the operating system's virtual memory management.
For example, when you have a 50GB index, instead of reading it chunk by chunk into memory, mmap makes it appear as if the entire index is in memory, even though physically it's still on disk. This is particularly effective on 64-bit systems with large amounts of RAM.
  - NIOFSDirectoryFactory:
This implementation uses Java's New I/O (NIO) package for file operations. Think of it as a modern, channel-based approach to file access. It's particularly good at handling many concurrent operations because it can use the operating system's native I/O operations. This makes it especially suitable for scenarios where you have many concurrent users searching your Solr index.
NIOFSDirectoryFactory is often the best choice when you need reliable performance across different operating systems and don't want to deal with memory-mapping complexities.
  - SimpleFSDirectoryFactory:
This is the most basic implementation, using simple file system operations. Imagine it as a straightforward, no-frills approach to file access. While it might not offer the performance optimizations of other implementations, it's very reliable and can be useful in situations where you want predictable behavior without any complex memory management or operating system-specific optimizations.
  - RAMDirectoryFactory (memory-based, non-persistent):
This is a special case - it keeps the entire index in memory without any persistence to disk. Think of it as creating a temporary, super-fast index that disappears when Solr shuts down. It's like having a high-speed, temporary workspace.

solr.StandardDirectoryFactory is filesystem based and tries to pick the best implementation for the current JVM and platform. 

solr.RAMDirectoryFactory is memory based, not persistent, and doesn't work with replication.

### codecFactory
```
  <codecFactory class="solr.SchemaCodecFactory"/>
```
**Required: No**

codecFactory in Solr is essentially responsible for controlling how data is physically written to and read from the Lucene index

It handles:
  - Data Compression
Determines how different field types are compressed
Manages the tradeoff between storage size and retrieval speed
Applies different compression strategies based on field characteristics
  - Field Encoding
Controls how various data types are encoded in the index
Handles special cases like docValues encoding
Manages posting list formats and term dictionary encoding
  - Index Format
Defines the physical structure of index files
Controls how term vectors are stored
Manages how stored fields are written to disk

For implementation class, options include:
  - class="solr.SchemaCodecFactory"
  - class="solr.SimpleTextCodecFactory"
    Creates human-readable index files
    Useful for debugging and understanding index structure
    Not recommended for production due to large size/poor performance
  - class="solr.PreferredCodecFactory"
    Allows explicit specification of codec name
    Useful when you want to force a specific Lucene codec version
    ```
      <codecFactory class="solr.PreferredCodecFactory">
        <str name="codec">Lucene95</str>
      </codecFactory>
    ```
  - Create own custom codec class

For compressionMode, options include "BEST_SPEED" or "BEST_COMPRESSION"

### indexConfig
Control how Lucene/Solr handles index creation and management. Here are the key components from the configuration:
  - Memory and Buffer Settings
    - ramBufferSizeMB: Controls how much RAM Lucene can use for buffering documents before flushing to disk
    - maxBufferedDocs: Sets a limit on number of documents that can be buffered before forcing a flush
    - Either limit can trigger a flush when reached
  - Lock Management
    - lockType: Specifies the LockFactory implementation to use for index locking. Options include:
      - native: Uses OS native file locking (default for Solr 3.6+)
      - single: For read-only indexes or single-process scenarios
      - simple: Uses a plain file for locking
    - Merge Management:
      - Merge Policy: Controls how index segments are merged. Default is TieredMergePolicy since Solr/Lucene 3.3.
        ```
        <mergePolicyFactory class="org.apache.solr.index.TieredMergePolicyFactory">
          <int name="maxMergeAtOnce">10</int>
          <int name="segmentsPerTier">10</int>
          <double name="noCFSRatio">0.1</double>
        </mergePolicyFactory>
        ```
        Parameters include:
        - maxMergeAtOnce: Controls the maximum number of segments to merge at the same time
        - segmentsPerTier: Defines how many segments are allowed in each tier
        - noCFSRatio: Controls which segments should use the compound file format
      - Merge Scheduler: Controls how merges are performed. Can be concurrent (background threads) or serial
    - Deletion Policy: Configurable through deletionPolicy. Controls how old commit points are removed. Parameters include:
      - maxCommitsToKeep: Number of commit points to retain
      - maxOptimizedCommitsToKeep: Number of optimized commit points to keep
      - maxCommitAge: Age-based deletion of commit points
    - infoStream: Optional debugging feature that can write detailed indexing information to a specified file 

### updateHandler
  - UpdateLog
    ```
    <updateLog>
      <str name="dir">${solr.ulog.dir:}</str>
      <int name="numVersionBuckets">${solr.ulog.numVersionBuckets:65536}</int>
    </updateLog>
    ```
    Enables transaction logging for:
      - Real-time get operations
      - Durability guarantees
      - SolrCloud replica recovery
   
    **dir**: Specifies where transaction logs are stored
    **numVersionBuckets**: Controls version tracking buckets (default: 65536). Higher values reduce synchronization overhead during high-volume indexing. Each bucket requires 8 bytes of heap space.
  - AutoCommit
    ```
     <autoCommit>
       <maxTime>${solr.autoCommit.maxTime:15000}  </maxTime>
       <openSearcher>false</openSearcher>
     </autoCommit>
    ```
    Performs `hard` commits automatically based on:
    - `maxTime`: Time since last document addition (default: 15000ms)
    - `openSearcher`: If false, flushes to storage without opening new searcher
 
    Hard commits ensure data durability but are resource-intensive. Alternative: Use `commitWithin` when adding documents
  - autoSoftCommit
    ```
      <autoSoftCommit>
          <maxTime>${solr.autoSoftCommit.maxTime:-1}</maxTime>
      </autoSoftCommit>
    ```
    Performs `soft` commits and it :
      - Makes changes visible to searches
      - Doesn't ensure data is synced to disk
      - is faster than hard commits
      - is better for near-realtime search scenarios
    
    -1 value disables soft auto-commits
  - Event Listeners
    - `postCommit`: Fires after every commit
    - `postOptimize`: Fires after optimize commands

### indexReaderFactory
IndexReaderFactory allows:
  - Allows customization of how Solr reads its index
  - Provides flexibility to implement alternative IndexReader behaviors
  
Default implementation uses disk-based index reading

```
<indexReaderFactory name="IndexReaderFactory" class="package.class">
    <str name="someArg">Some Value</str>
</indexReaderFactory>
```

Note:
  - Experimental Feature Status
  - May conflict with ReplicationHandler (SOLR-1366)
  - ReplicationHandler assumes disk-resident index
  - Custom implementations might break replication functionality

### query
  - maxBooleanClauses
    ```
     <maxBooleanClauses>2048</maxBooleanClauses>
    ```
    Sets maximum number of clauses in Boolean queries
Global Lucene property affecting all SolrCores
Note: Last initialized SolrCore determines the value
  - Cache
    - class implementation
      - LRUCache: Based on synchronized LinkedHashMap
      - FastLRUCache: Based on ConcurrentHashMap
        Better for high hit ratios (>75%)
        Faster gets, slower puts in single-threaded operations
    - size: Maximum entries in cache
    - initialSize: Initial capacity
    - autowarmCount: Items to prepopulate from old cache
    - maxRamMB: Maximum RAM usage (optional) 
    - filterCache
      ```
       <filterCache class="solr.FastLRUCache"
             size="512"
             initialSize="512"
             autowarmCount="0"/>
      ```
      Caches document sets matching queries
      Used for filter operations
    - queryResultCache
      ```
       <queryResultCache class="solr.LRUCache"
                  size="512"
                  initialSize="512"
                  autowarmCount="0"/>
      ```
      Stores ordered lists of document IDs
      Based on query, sort, and document range
    - documentCache
      ```
       <documentCache class="solr.LRUCache"
               size="512"
               initialSize="512"
               autowarmCount="0"/>
      ```
      Caches Lucene Document objects
      Stores field values
    
- enableLazyFieldLoading `<enableLazyFieldLoading>true</enableLazyFieldLoading>`
  Loads unrequested stored fields only when needed
  Improves performance for large text fields
  
- queryResult
  ```
    <queryResultWindowSize>20</queryResultWindowSize>
    <queryResultMaxDocsCached>200</queryResultMaxDocsCached>
  ```
  Controls caching behavior for query results optimizes for pagination scenarios
  
  queryResultWindowSize: When a search is requested, a superset of the requested number of document ids are collected.  For example, if a search for a particular query requests matching documents 10 through 19, and queryWindowSize is 50, then documents 0 through 49 will be collected and cached.  Any further requests in that range can be satisfied via the cache.
  
  queryResultMaxDocsCached: Maximum number of documents to cache for any entry in the queryResultCache
  
- Event Listeners
  ```
  <listener event="newSearcher" class="solr.QuerySenderListener">
  <listener event="firstSearcher" class="solr.QuerySenderListener">
  ```
  QuerySenderListener takes an array of NamedList and executes a local query request for each NamedList in sequence

  newSearcher: Fired when new searcher is prepared
firstSearcher: Fired for initial searcher

- useColdSearcher
  ```
  <useColdSearcher>false</useColdSearcher>
  ```
  Controls behavior when no warmed searcher is available
    - false: Requests block until searcher is warmed
    - true: Uses unwarmed searcher immediately

### requestDispatcher
  - requestParsers
    ```
     <requestParsers enableRemoteStreaming="true"
                multipartUploadLimitInKB="2048000"
                formdataUploadLimitInKB="2048"
                addHttpRequestToContext="false"/>
    ```
     - enableRemoteStreaming: Allows use of stream.file and stream.url parameters. Note: Requires authentication when enabled
Enables fetching remote files
     - multipartUploadLimitInKB: Maximum size for multipart file uploads
     - formdataUploadLimitInKB: Maximum size for POST form data. Handles application/x-www-form-urlencoded data.
     - addHttpRequestToContext: Controls HttpServletRequest inclusion. Adds request object to SolrQueryRequest context.
   - httpCaching
     ```
     <httpCaching never304="true" />
     ```
     never304="true": Disables HTTP 304 (Not Modified) responses. Prevents Solr from sending caching-related headers
     
     never304="false" for automatic cache header generation
     - cacheControl
       ```
        <httpCaching never304="true">
          <cacheControl>max-age=30, public</cacheControl>
        </httpCaching>
       ```
       Sets Cache-Control header
       Can specify max-age and visibility
       Works even with never304="true"
     - Dynamic Caching Headers
       ```
        <httpCaching lastModifiedFrom="openTime"
             etagSeed="Solr">
          <cacheControl>max-age=30, public</cacheControl>
        </httpCaching>
       ```
       - lastModifiedFrom: 
         - "openTime": Based on current Searcher opening time
         - "dirLastMod": Based on physical index modification time
       - etagSeed: Forces different ETag values
       - Cache Validation Options:
         - Generates Last-Modified headers
         - Handles If-Modified-Since requests
         - Manages ETag validation
         - Responds to If-None-Match requests

### Request Handlers
  - Default Search Handler [/seach]
    ```
    <requestHandler name="/select" class="solr.SearchHandler">
    <lst name="defaults">
      <str name="echoParams">explicit</str>
      <int name="rows">10</int>
      <str name="wt">json</str>
      <str name="indent">true</str>
    </lst>
    </requestHandler>
    ```
    - echoParams: Shows which parameters were used in the response
    - rows: Returns 10 results by default
    - wt: Returns results in JSON format
    - indent: Pretty prints the JSON response

    The following sections are commented out in code.
    ```
    <!-- <lst name="appends">
     ...
    </lst> -->
    ```
    This section would append additional parameters to every query. These parameters cannot be overridden by clients.
    ```
    <!-- <lst name="invariants">
     ...
    </lst> -->
    ```
    This section would define fixed parameters that cannot be changed by clients.
    ```
    <!-- <arr name="components">
     <str>nameOfCustomComponent1</str>
     ...
    </arr> -->
    ```
    This section allows customization of the search components chain, either replacing or extending the default components.
  - Data Import Handler [/dataimport]
    ```
    <requestHandler name="/dataimport" class="solr.DataImportHandler">
    <lst name="defaults">
      <str name="config">solr-data-config.xml</str>
    </lst>
    </requestHandler>
    ```
    Creates an endpoint at /dataimport that handles data import operations. `solr.DataImportHandler` is Solr's built-in handler for managing data imports.
    
    Data import configuration is stored in a file named solr-data-config.xml. This external configuration file defines:
      - Data sources (databases, files, etc.)
      - Entity relationships
      - Field mappings
      - Import queries or specifications

    Operations available through this handler:
      - full-import: Complete data import
      - delta-import: Incremental update
      - status: Check import status
      - reload-config: Reload configuration
      - abort: Stop running import
  - Query handler [/query]
    ```
     <requestHandler name="/query" class="solr.SearchHandler">
      <lst name="defaults">
        <str name="echoParams">explicit</str>
        <str name="wt">json</str>
        <str name="indent">true</str>
      </lst>
    </requestHandler>
    ```
    Creates an endpoint at /query
    Uses Solr's standard SearchHandler class for processing queries

    - echoParams: Set to "explicit" to show which parameters were used in the response
    - wt (writer type): Set to "json" to return results in JSON format
    - indent: Set to "true" to format the JSON response with proper indentation for readability

    Difference from `/select` is that no default rows parameter (will use Solr's system default)
    
### Browse Handler [/browse]
  ```
  <requestHandler name="/browse" class="solr.SearchHandler" useParams="query,facets,velocity,browse">
    <lst name="defaults">
      <str name="echoParams">explicit</str>
    </lst>
  </requestHandler>
  ```
  Creates an endpoint at /browse
  Uses standard solr.SearchHandler class
  `useParams` references parameter sets defined in `initParams` in the configuration:
- query: Might contain common query parameters
- facets: Would define faceting behavior
- velocity: Parameters for Velocity template rendering
- browse: Browse-specific parameters
  
  #### initParams
  ```
  <initParams path="/update/**,/query,/select,/tvrh,/elevate,/spell,/browse">
    <lst name="defaults">
      <str name="df">_text_</str>
    </lst>
  </initParams>
  ```
  - Path specification
    `<initParams path="/update/**,/query,/select,/tvrh,/elevate,/spell,/browse">`
    - /update/**: All update handlers (the ** wildcard means all sub-paths)
    - /query: Query handler
    - /select: Select handler
    - /tvrh: Term Vector Request Handler
    - /elevate: Query elevation handler
    - /spell: Spell checking handler
    - /browse: Browse handler
  - Default Param
    ```
    <lst name="defaults">
      <str name="df">_text_</str>
    </lst>
    ```
    df (default field) is set to `_text_`
    This means when no specific field is specified in a query, Solr will search in the _text_ field

    It means:
    - Provides a consistent default search field across multiple handlers
    - Makes maintenance easier since you only need to change the default field in one place
    - The `_text_` field typically contains content from multiple fields

### Update handler [/update]
```
  <requestHandler name="/update/extract"
                  startup="lazy"
                  class="solr.extraction.ExtractingRequestHandler" >
    <lst name="defaults">
      <str name="lowernames">true</str>
      <str name="fmap.meta">ignored_</str>
      <str name="fmap.content">_text_</str>
    </lst>
  </requestHandler>
```
Endpoint: /update/extract
startup="lazy": Handler loads only when first requested (saves resources)
Uses Solr's ExtractingRequestHandler class for Tika-based content extraction

This handler is particularly useful for:
 - Indexing documents
 - Search applications
 - Knowledge bases

Attributes include:
  - lowernames: Converts all field names to lowercase
  - fmap.meta: Maps metadata fields to prefix `ignored_` (ignores them)
  - fmap.content: Maps extracted content to the `text` field

### Spell Check Component
```
  <searchComponent name="spellcheck" class="solr.SpellCheckComponent">
    <str name="queryAnalyzerFieldType">text_general</str>
    <lst name="spellchecker">
      <str name="name">default</str>
      <str name="field">_text_</str>
      <str name="classname">solr.DirectSolrSpellChecker</str>
      <str name="distanceMeasure">internal</str>
      <float name="accuracy">0.5</float>
      <int name="maxEdits">2</int>
      <int name="minPrefix">1</int>
      <int name="maxInspections">5</int>
      <int name="minQueryLength">4</int>
      <float name="maxQueryFrequency">0.01</float>
    </lst>
  </searchComponent>
```

Attributes inclues:
  - query: Basic query processing
  - facet: Faceted search functionality
  - mlt: More Like This feature
  - highlight: Result highlighting
  - stats: Statistical functions
  - debug: Debugging information
  - accuracy: 0.5 minimum accuracy for suggestions
  - maxEdits: Maximum 2 character edits allowed
  - minPrefix: Requires 1 character prefix match
  - maxInspections: Checks up to 5 terms per result
  - minQueryLength: Terms must be at least 4 characters
  - maxQueryFrequency: Term must appear in less than 1% of docs
  - classname: solr.DirectSolrSpellChecker or solr.WordBreakSolrSpellChecker

SpellCheckComponent can be hooked into the request handler that handles normal user queries so that a separate request is not needed to get suggestions.

For example:
```
  <requestHandler name="/spell" class="solr.SearchHandler" startup="lazy">
    <lst name="defaults">
      <str name="spellcheck.dictionary">default</str>
      <str name="spellcheck">on</str>
      <str name="spellcheck.extendedResults">true</str>
      <str name="spellcheck.count">10</str>
      <str name="spellcheck.alternativeTermCount">5</str>
      <str name="spellcheck.maxResultsForSuggest">5</str>
      <str name="spellcheck.collate">true</str>
      <str name="spellcheck.collateExtendedResults">true</str>
      <str name="spellcheck.maxCollationTries">10</str>
      <str name="spellcheck.maxCollations">5</str>
    </lst>
    <arr name="last-components">
      <str>spellcheck</str>
    </arr>
  </requestHandler>
```

### Term Vector Component
```
 <searchComponent name="tvComponent" class="solr.TermVectorComponent"/>
 <requestHandler name="/tvrh" class="solr.SearchHandler" startup="lazy">
    <lst name="defaults">
      <bool name="tv">true</bool>
    </lst>
    <arr name="last-components">
      <str>tvComponent</str>
    </arr>
  </requestHandler>
```

`<searchComponent name="tvComponent" class="solr.TermVectorComponent"/>`
Defines a component named "tvComponent"
Uses Solr's TermVectorComponent class
Provides access to term vector information from the index

`<requestHandler name="/tvrh" class="solr.SearchHandler" startup="lazy">`
Creates a /tvrh endpoint
Uses standard SearchHandler
Lazy loading enabled (loads only when first used)

Attribute `tv` enables term vector retrieval by default.

This can be used for:
- Analyzing term frequencies
- Examining document vectors
- Text analysis
- Feature extraction

### Terms Component
```
  <searchComponent name="terms" class="solr.TermsComponent"/>

  <requestHandler name="/terms" class="solr.SearchHandler" startup="lazy">
    <lst name="defaults">
      <bool name="terms">true</bool>
      <bool name="distrib">false</bool>
    </lst>
    <arr name="components">
      <str>terms</str>
    </arr>
  </requestHandler>
```

`<searchComponent name="terms" class="solr.TermsComponent"/>`
Defines a component named "terms"
Uses Solr's TermsComponent class
Used for accessing term information and statistics

`<requestHandler name="/terms" class="solr.SearchHandler" startup="lazy">`
Creates a /terms endpoint
Uses standard SearchHandler
Lazy loading enabled (loads only when requested)

`terms`: Terms component is enabled by default
`distrib`: Distributed search is disabled by default

### Query Elevation Component
```
  <searchComponent name="elevator" class="solr.QueryElevationComponent" >
    <str name="queryFieldType">string</str>
    <str name="config-file">elevate.xml</str>
  </searchComponent>

  <requestHandler name="/elevate" class="solr.SearchHandler" startup="lazy">
    <lst name="defaults">
      <str name="echoParams">explicit</str>
    </lst>
    <arr name="last-components">
      <str>elevator</str>
    </arr>
  </requestHandler>
```

```
<searchComponent name="elevator" class="solr.QueryElevationComponent">
  <str name="queryFieldType">string</str>
  <str name="config-file">elevate.xml</str>
</searchComponent>
```
Uses QueryElevationComponent class
Queries analyzed as 'string' type
Configuration stored in 'elevate.xml'

`<requestHandler name="/elevate" class="solr.SearchHandler" startup="lazy">`
Creates an /elevate endpoint
Uses standard SearchHandler
Lazy loading enabled

`echoParams`: Shows which parameters were used in the response

This enables you to configure the top results for a given query regardless of the normal lucene scoring.

### Highlighting Component

```
  <searchComponent class="solr.HighlightComponent" name="highlight">
    <highlighting>
      <fragmenter name="gap"
                  default="true"
                  class="solr.highlight.GapFragmenter">
        <lst name="defaults">
          <int name="hl.fragsize">100</int>
        </lst>
      </fragmenter>

      <fragmenter name="regex"
                  class="solr.highlight.RegexFragmenter">
        <lst name="defaults">
          <int name="hl.fragsize">70</int>
          <float name="hl.regex.slop">0.5</float>
          <str name="hl.regex.pattern">[-\w ,/\n\&quot;&apos;]{20,200}</str>
        </lst>
      </fragmenter>

      <formatter name="html"
                 default="true"
                 class="solr.highlight.HtmlFormatter">
        <lst name="defaults">
          <str name="hl.simple.pre"><![CDATA[<em>]]></str>
          <str name="hl.simple.post"><![CDATA[</em>]]></str>
        </lst>
      </formatter>

      <encoder name="html"
               class="solr.highlight.HtmlEncoder" />

      <fragListBuilder name="simple"
                       class="solr.highlight.SimpleFragListBuilder"/>

      <fragListBuilder name="single"
                       class="solr.highlight.SingleFragListBuilder"/>

      <fragListBuilder name="weighted"
                       default="true"
                       class="solr.highlight.WeightedFragListBuilder"/>

      <fragmentsBuilder name="default"
                        default="true"
                        class="solr.highlight.ScoreOrderFragmentsBuilder">
      </fragmentsBuilder>

      <fragmentsBuilder name="colored"
                        class="solr.highlight.ScoreOrderFragmentsBuilder">
        <lst name="defaults">
          <str name="hl.tag.pre"><![CDATA[
               <b style="background:yellow">,<b style="background:lawgreen">,
               <b style="background:aquamarine">,<b style="background:magenta">,
               <b style="background:palegreen">,<b style="background:coral">,
               <b style="background:wheat">,<b style="background:khaki">,
               <b style="background:lime">,<b style="background:deepskyblue">]]></str>
          <str name="hl.tag.post"><![CDATA[</b>]]></str>
        </lst>
      </fragmentsBuilder>

      <boundaryScanner name="default"
                       default="true"
                       class="solr.highlight.SimpleBoundaryScanner">
        <lst name="defaults">
          <str name="hl.bs.maxScan">10</str>
          <str name="hl.bs.chars">.,!? &#9;&#10;&#13;</str>
        </lst>
      </boundaryScanner>

      <boundaryScanner name="breakIterator"
                       class="solr.highlight.BreakIteratorBoundaryScanner">
        <lst name="defaults">
          <str name="hl.bs.type">WORD</str>
          <str name="hl.bs.language">en</str>
          <str name="hl.bs.country">US</str>
        </lst>
      </boundaryScanner>
    </highlighting>
  </searchComponent>
```

**Default fragmenter**
```
<fragmenter name="gap" default="true" class="solr.highlight.GapFragmenter">
  <lst name="defaults">
    <int name="hl.fragsize">100</int>
  </lst>
</fragmenter>
```
Creates fixed-size fragments (100 characters)
For basic highlighting needs

**Regex Fragmenter**
```
<fragmenter name="regex" class="solr.highlight.RegexFragmenter">
  <lst name="defaults">
    <int name="hl.fragsize">70</int>
    <float name="hl.regex.slop">0.5</float>
    <str name="hl.regex.pattern">[-\w ,/\n\&quot;&apos;]{20,200}</str>
  </lst>
</fragmenter>
```
Uses regular expressions for intelligent fragmentation
Fragment size: 70 characters
Allows 50% size variation (slop)
Pattern matches words, punctuation, and whitespace
For sentence-based highlighting

**HTML Formatter**
```
<formatter name="html" default="true" class="solr.highlight.HtmlFormatter">
  <lst name="defaults">
    <str name="hl.simple.pre"><![CDATA[<em>]]></str>
    <str name="hl.simple.post"><![CDATA[</em>]]></str>
  </lst>
</formatter>
```
Default HTML formatting
Wraps highlighted terms in <em> tags
Customizable pre/post tags
    
**fragListBuilder**
```
<fragListBuilder name="simple" class="solr.highlight.SimpleFragListBuilder"/>
<fragListBuilder name="single" class="solr.highlight.SingleFragListBuilder"/>
<fragListBuilder name="weighted" default="true" class="solr.highlight.WeightedFragListBuilder"/>
```
Simple: Basic fragment collection
Single: Creates one fragment per field
Weighted (Default): Uses scoring to select best fragments
    
**Default Fragment Builder**
`<fragmentsBuilder name="default" default="true" class="solr.highlight.ScoreOrderFragmentsBuilder">`
  Orders fragments by score
  Optional separator character for multi-valued fields

**Colored Fragment Builder**
```
<fragmentsBuilder name="colored"
                        class="solr.highlight.ScoreOrderFragmentsBuilder">
   <lst name="defaults">
     <str name="hl.tag.pre"><![CDATA[
               <b style="background:yellow">,<b style="background:lawgreen">,
               <b style="background:aquamarine">,<b style="background:magenta">,
               <b style="background:palegreen">,<b style="background:coral">,
               <b style="background:wheat">,<b style="background:khaki">,
               <b style="background:lime">,<b style="background:deepskyblue">]]></str>
     <str name="hl.tag.post"><![CDATA[</b>]]></str>
   </lst>
</fragmentsBuilder>
```
Provides multiple background colors
Useful for distinguishing different matches
Includes 10 predefined colors

**Simple Boundary Scanner**
```
<boundaryScanner name="default" default="true" class="solr.highlight.SimpleBoundaryScanner">
  <lst name="defaults">
    <str name="hl.bs.maxScan">10</str>
    <str name="hl.bs.chars">.,!? &#9;&#10;&#13;</str>
  </lst>
</boundaryScanner>
```
Scans up to 10 characters for boundaries
Uses punctuation and whitespace as boundaries
    
**Break Iterator Scanner**
```
<boundaryScanner name="breakIterator" class="solr.highlight.BreakIteratorBoundaryScanner">
  <lst name="defaults">
    <str name="hl.bs.type">WORD</str>
    <str name="hl.bs.language">en</str>
    <str name="hl.bs.country">US</str>
  </lst>
</boundaryScanner>
```
Language-aware boundary detection
Supports WORD, CHARACTER, LINE, and SENTENCE boundaries
Locale-specific processing
Multi-language content

### Suggest Component
```
  <searchComponent name="suggest" class="solr.SuggestComponent">
    <lst name="suggester">
      <str name="name">name</str>
      <str name="field">name_suggest</str>
      <str name="lookupImpl">BlendedInfixLookupFactory</str>
      <str name="blenderType">position_linear</str>
      <str name="weightFieldValue">weight</str>
      <str name="suggestAnalyzerFieldType">text_stemmed</str>
      <str name="highlight">false</str>
      <str name="buildOnCommit">false</str>
      <str name="buildOnStartup">false</str>
    </lst>
  </searchComponent>

  <requestHandler name="/suggest" class="solr.SearchHandler" startup="lazy">
    <lst name="defaults">
      <str name="wt">json</str>
      <str name="indent">true</str>
      <str name="suggest">true</str>
      <str name="suggest.dictionary">name</str>
      <str name="suggest.count">10</str>
    </lst>
    <arr name="components">
      <str>suggest</str>
    </arr>
  </requestHandler>
```
This component is used for:
- Autocomplete functionality
- Search suggestions
- Type-ahead features
- Weighted suggestions
- Partial word matching

Component Attributes include:
 - `field`: Uses the field "name_suggest" for suggestions
 - `lookupImpl`: Uses BlendedInfixLookupFactory for partial matching
 - `blenderType`: Linear position-based blending
 - `weightFieldValue`: Weights suggestions using "weight" field
 - `suggestAnalyzerFieldType`: Uses text_stemmed analyzer
 - Highlighting disabled
 - Dictionary not rebuilt automatically

Handler Attributes include:
 - `wt`: Returns JSON format
 - `indent`: Indented output
 - `suggest`: Suggestion enabled
 - `suggest.dictionary`: name dictionary
 - `suggest.count`: Returns top 10 suggestions

### Update Request Processer Chain
```
  <updateRequestProcessorChain name="add-unknown-fields-to-the-schema">
    <processor class="solr.UUIDUpdateProcessorFactory" />
    <processor class="solr.RemoveBlankFieldUpdateProcessorFactory"/>
    <processor class="solr.FieldNameMutatingUpdateProcessorFactory">
      <str name="pattern">[^\w-\.]</str>
      <str name="replacement">_</str>
    </processor>
    <processor class="solr.ParseBooleanFieldUpdateProcessorFactory"/>
    <processor class="solr.ParseLongFieldUpdateProcessorFactory"/>
    <processor class="solr.ParseDoubleFieldUpdateProcessorFactory"/>
    <processor class="solr.ParseDateFieldUpdateProcessorFactory">
      <arr name="format">
        <str>yyyy-MM-dd'T'HH:mm:ss.SSSZ</str>
        <str>yyyy-MM-dd'T'HH:mm:ss,SSSZ</str>
        <str>yyyy-MM-dd'T'HH:mm:ss.SSS</str>
        <str>yyyy-MM-dd'T'HH:mm:ss,SSS</str>
        <str>yyyy-MM-dd'T'HH:mm:ssZ</str>
        <str>yyyy-MM-dd'T'HH:mm:ss</str>
        <str>yyyy-MM-dd'T'HH:mmZ</str>
        <str>yyyy-MM-dd'T'HH:mm</str>
        <str>yyyy-MM-dd HH:mm:ss.SSSZ</str>
        <str>yyyy-MM-dd HH:mm:ss,SSSZ</str>
        <str>yyyy-MM-dd HH:mm:ss.SSS</str>
        <str>yyyy-MM-dd HH:mm:ss,SSS</str>
        <str>yyyy-MM-dd HH:mm:ssZ</str>
        <str>yyyy-MM-dd HH:mm:ss</str>
        <str>yyyy-MM-dd HH:mmZ</str>
        <str>yyyy-MM-dd HH:mm</str>
        <str>yyyy-MM-dd</str>
      </arr>
    </processor>
    <processor class="solr.AddSchemaFieldsUpdateProcessorFactory">
      <str name="defaultFieldType">strings</str>
      <lst name="typeMapping">
        <str name="valueClass">java.lang.Boolean</str>
        <str name="fieldType">booleans</str>
      </lst>
      <lst name="typeMapping">
        <str name="valueClass">java.util.Date</str>
        <str name="fieldType">tdates</str>
      </lst>
      <lst name="typeMapping">
        <str name="valueClass">java.lang.Long</str>
        <str name="valueClass">java.lang.Integer</str>
        <str name="fieldType">tlongs</str>
      </lst>
      <lst name="typeMapping">
        <str name="valueClass">java.lang.Number</str>
        <str name="fieldType">tdoubles</str>
      </lst>
    </processor>

    <processor class="solr.LogUpdateProcessorFactory"/>
    <processor class="solr.DistributedUpdateProcessorFactory"/>
    <processor class="solr.RunUpdateProcessorFactory"/>
  </updateRequestProcessorChain>
```

**UUID Processor**
`<processor class="solr.UUIDUpdateProcessorFactory" />`
Generates unique IDs for documents if none provided
    
**Remove Blank Field Processor**
`<processor class="solr.RemoveBlankFieldUpdateProcessorFactory"/>`
Removes null values, empty strings, black spaces. Reduces index size.
    
**Field Name Mutating Processor**
```
<processor class="solr.FieldNameMutatingUpdateProcessorFactory">
  <str name="pattern">[^\w-\.]</str>
  <str name="replacement">_</str>
</processor>
```
Replaces invalid characters with underscores
Ensures field name compatibility
Maintains naming consistency
Prevents indexing errors

Configuration:
 - pattern: Matches non-word characters except hyphens and dots
 - replacement: Uses underscore as replacement character

**Parse Boolean Field Processor**
`<processor class="solr.ParseBooleanFieldUpdateProcessorFactory"/>`
Identifies boolean-like values
Converts to proper boolean type
Handles various boolean representations
Ensures type consistency

**Parse Long Field Processor**
`<processor class="solr.ParseLongFieldUpdateProcessorFactory"/>`
Identifies numeric values
Converts to long type
Handles integer overflow
Maintains precision
    
**Parse Double Field Processor**
`<processor class="solr.ParseDoubleFieldUpdateProcessorFactory"/>`
Identifies decimal values
Converts to double type
Handles scientific notation
Maintains precision
    
**Parse Date Field Processor**
```
   <processor class="solr.ParseDateFieldUpdateProcessorFactory">
      <arr name="format">
        <str>yyyy-MM-dd'T'HH:mm:ss.SSSZ</str>
        <str>yyyy-MM-dd'T'HH:mm:ss,SSSZ</str>
        <str>yyyy-MM-dd'T'HH:mm:ss.SSS</str>
        <str>yyyy-MM-dd'T'HH:mm:ss,SSS</str>
        <str>yyyy-MM-dd'T'HH:mm:ssZ</str>
        <str>yyyy-MM-dd'T'HH:mm:ss</str>
        <str>yyyy-MM-dd'T'HH:mmZ</str>
        <str>yyyy-MM-dd'T'HH:mm</str>
        <str>yyyy-MM-dd HH:mm:ss.SSSZ</str>
        <str>yyyy-MM-dd HH:mm:ss,SSSZ</str>
        <str>yyyy-MM-dd HH:mm:ss.SSS</str>
        <str>yyyy-MM-dd HH:mm:ss,SSS</str>
        <str>yyyy-MM-dd HH:mm:ssZ</str>
        <str>yyyy-MM-dd HH:mm:ss</str>
        <str>yyyy-MM-dd HH:mmZ</str>
        <str>yyyy-MM-dd HH:mm</str>
        <str>yyyy-MM-dd</str>
      </arr>
    </processor>
```
Supports multiple date formats
Handles timezone conversions
Processes millisecond precision
Standardizes date representation
    
**Add Schema Fields Processor**
```
<processor class="solr.AddSchemaFieldsUpdateProcessorFactory">
  <str name="defaultFieldType">strings</str>
  <lst name="typeMapping">
    <!-- Type mappings -->
  </lst>
</processor>
```
Adds new fields automatically
Maps Java types to Solr types
Handles type inference
Maintains schema consistency

Type Mappings:
  - Boolean Mapping
    ```
    <lst name="typeMapping">
      <str name="valueClass">java.lang.Boolean</str>
      <str name="fieldType">booleans</str>
    </lst>
    ```
  - Date Mapping 
    ```
    <lst name="typeMapping">
      <str name="valueClass">java.util.Date</str>
      <str name="fieldType">tdates</str>
    </lst>
    ```
  - Integer Mapping
    ```
    <lst name="typeMapping">
      <str name="valueClass">java.lang.Long</str>
      <str name="valueClass">java.lang.Integer</str>
      <str name="fieldType">tlongs</str>
    </lst>
    ```
  - Number Mapping
    ```
    <lst name="typeMapping">
      <str name="valueClass">java.lang.Number</str>
      <str name="fieldType">tdoubles</str>
    </lst>
    ```
    
**Log Update Processor**
`<processor class="solr.LogUpdateProcessorFactory"/>`
Records update operations
Provides debugging information
Tracks document changes
Assists in troubleshooting

**Distributed Update Processor**
`<processor class="solr.DistributedUpdateProcessorFactory"/>`
Manages shard distribution
Handles replication
Ensures consistency
Manages cluster updates
    
**Run Update Processor**
`<processor class="solr.RunUpdateProcessorFactory"/>`
Commits changes
Finalizes updates
Ensures persistence
Triggers index updates

### Query Response Writer
```
  <queryResponseWriter name="json" class="solr.JSONResponseWriter" />

  <queryResponseWriter name="velocity" class="solr.VelocityResponseWriter" startup="lazy">
    <str name="template.base.dir">${velocity.template.base.dir:}</str>
    <str name="solr.resource.loader.enabled">${velocity.solr.resource.loader.enabled:true}</str>
    <str name="params.resource.loader.enabled">${velocity.params.resource.loader.enabled:false}</str>
  </queryResponseWriter>

  <queryResponseWriter name="xslt" class="solr.XSLTResponseWriter">
    <int name="xsltCacheLifetimeSeconds">5</int>
  </queryResponseWriter>
```

**JSON Response Writer**
Default JSON format writer
No additional configuration needed
Returns results in JSON format

**Velocity Response Writer**
Template-based response formatting
Lazy loading
Configurable template directory
Resource loader settings
Parameter-based template loading control

**XSLT Response Writer**
Transforms XML output using XSLT
Uses templates from conf/xslt directory
5-second cache lifetime for XSLT files
Allows custom XML transformations

    
# Search Core `solr-data-config.xml`

### LEAR Data Source
```
<dataSource
  name="lear-ds"
  type="com.s24.search.solr.analysis.jdbc.DataImportJdbcDataSource"
  dataSource="jdbc/lear"
/>
```
Uses a custom JDBC data source implementation
References a JNDI datasource named `jdbc/lear`
Primary source for certain business types
    
### COLIN Data Source
```
<dataSource
  name="colin-ds"
  type="com.s24.search.solr.analysis.jdbc.DataImportJdbcDataSource"
  dataSource="jdbc/colin"
/>
```
References a JNDI datasource named `jdbc/colin`
    
### LEAR Entity
```
SELECT 
  identifier,
  legal_name as name,
  legal_type as legalType,
  state as status,
  tax_id as bn
FROM businesses
WHERE legal_type in ('BEN', 'CP', 'SP', 'GP')
```
Field mappings
Handles Benefit Company, Cooperative, Sole Proprietorship, General Partnership
    
### COLIN Entity
```
SELECT 
  c.corp_num as identifier,
  c.corp_typ_cd as legalType,
  c.bn_15 as bn,
  CASE cs.state_typ_cd
    when 'ACT' then 'ACTIVE'
    when 'HIS' then 'HISTORICAL'
    when 'HLD' then 'LIQUIDATION'
    else cs.state_typ_cd
  END as status,
  cn.corp_nme as name
FROM corporation c
  join corp_state cs on cs.corp_num = c.corp_num
  join corp_name cn on cn.corp_num = c.corp_num
WHERE c.corp_typ_cd not in ('BEN','CP','GP','SP')
  and cs.end_event_id is null
  and cn.end_event_id is null
  and cn.corp_name_typ_cd in ('CO', 'NB')
```
Joins corporation, corp_state, corp_name tables
Status mappings
Field mappings
Filters - excludes business types handled by LEAR, includes only active records and legal type

# Search Core Schema Config

### Fields Definition
#### Base Fields
```
<field name="identifier" type="text_basic" stored="true" required="true" indexed="true" />
<field name="name" type="text_basic" stored="true" required="true" indexed="true" />
<field name="legalType" type="string" stored="true" required="true" indexed="true" docValues="true" />
<field name="status" type="string" stored="true" required="true" indexed="true" docValues="true" />
<field name="bn" type="text_basic" stored="true" indexed="true" />
```
identifier: Unique key field (text_basic)
name: Business name (text_basic)
legalType: Legal entity type (string)
status: Business status (string)
bn: Business number (text_basic)
    
#### Suggestion and Selection Fields
```
<field name="name_suggest" type="phrase_basic" indexed="true" stored="true" />
<field name="name_select" type="text_stemmed" indexed="true" stored="true" />
<field name="name_single_term" type="text_ngram" indexed="true" stored="true" />
<field name="name_stem_agro" type="text_stemmed_agro" indexed="true" stored="true" />
<field name="name_synonym" type="text_synonym" indexed="true" stored="true" />

<field name="identifier_select" type="phrase_ngram" indexed="true" stored="true" />

<field name="bn_select" type="phrase_ngram" indexed="true" stored="true" />
```
name_suggest: Used for providing name suggestions in search (phrase_basic, Stored: Yes, Indexed: Yes)
name_select: Used for advanced selection queries with stemming (text_stemmed, Stored: Yes, Indexed: Yes)
name_single_term: Supports single-term queries using n-gram analysis (text_ngram, Stored: Yes, Indexed: Yes)
name_stem_agro: Applies aggressive stemming to names for broader matching (text_stemmed_agro, Stored: Yes, Indexed: Yes)
name_synonym: Supports synonym expansion during queries (text_synonym, Stored: Yes, Indexed: Yes)
identifier_select: Enables identifier selection with n-gram analysis (phrase_ngram, Stored: Yes, Indexed: Yes)
bn_select: Supports selection queries on the bn field (phrase_ngram, Stored: Yes, Indexed: Yes)
weight: A floating-point field used for boosting or ranking (float, Stored: Yes, Indexed: Yes)

#### Unique Key Field
`<uniqueKey>identifier</uniqueKey>`
Specifies the identifier field as the unique key for each document in the index. This ensures that each document is uniquely identifiable.
    
#### Field Types
##### Custom
**Text**
```
   <fieldType class="solr.TextField" name="text_basic" positionIncrementGap="100">
      <analyzer>
        <tokenizer class="solr.LowerCaseTokenizerFactory"/>
      </analyzer>
    </fieldType>

    <fieldType class="solr.TextField" name="text_stemmed" positionIncrementGap="100">
      <analyzer type="index">
        <tokenizer class="solr.WhitespaceTokenizerFactory" />
        <filter class="solr.StandardFilterFactory" />
        <filter class="solr.LowerCaseFilterFactory" />
        <filter class="solr.WordDelimiterGraphFilterFactory" catenateAll="1" splitOnNumerics="0" generateWordParts="0" generateNumberParts="0" />
        <filter class="solr.FlattenGraphFilterFactory" />
        <filter class="solr.EnglishMinimalStemFilterFactory" />
      </analyzer>
      <analyzer type="query">
        <tokenizer class="solr.WhitespaceTokenizerFactory" />
        <filter class="solr.StandardFilterFactory" />
        <filter class="solr.LowerCaseFilterFactory" />
        <filter class="solr.WordDelimiterGraphFilterFactory" catenateAll="1" splitOnNumerics="0" generateWordParts="0" generateNumberParts="0" />
        <filter class="solr.EnglishMinimalStemFilterFactory" />
      </analyzer>
    </fieldType>

    <fieldType class="solr.TextField" name="text_stemmed_agro" positionIncrementGap="100">
      <analyzer type="index">
        <tokenizer class="solr.WhitespaceTokenizerFactory" />
        <filter class="solr.StandardFilterFactory" />
        <filter class="solr.LowerCaseFilterFactory" />
        <filter class="solr.WordDelimiterGraphFilterFactory" catenateAll="1" splitOnNumerics="0" generateWordParts="0" generateNumberParts="0" />
        <filter class="solr.FlattenGraphFilterFactory" />
        <filter class="solr.PorterStemFilterFactory" />
      </analyzer>
      <analyzer type="query">
        <tokenizer class="solr.WhitespaceTokenizerFactory" />
        <filter class="solr.StandardFilterFactory" />
        <filter class="solr.LowerCaseFilterFactory" />
        <filter class="solr.WordDelimiterGraphFilterFactory" catenateAll="1" splitOnNumerics="0" generateWordParts="0" generateNumberParts="0" />
        <filter class="solr.PorterStemFilterFactory" />
      </analyzer>
    </fieldType>

    <fieldType class="solr.TextField" name="text_ngram">
      <analyzer type="index">
        <tokenizer class="solr.WhitespaceTokenizerFactory"/>
        <filter class="solr.LowerCaseFilterFactory"/>
        <filter class="solr.WordDelimiterGraphFilterFactory" catenateAll="1" splitOnNumerics="0" generateWordParts="0" generateNumberParts="0" />
        <filter class="solr.FlattenGraphFilterFactory" />
        <filter class="solr.NGramFilterFactory" minGramSize="1" maxGramSize="15" />
      </analyzer>
      <analyzer type="query">
        <tokenizer class="solr.WhitespaceTokenizerFactory"/>
        <filter class="solr.LowerCaseFilterFactory"/>
        <filter class="solr.WordDelimiterGraphFilterFactory" catenateAll="1" splitOnNumerics="0" generateWordParts="0" generateNumberParts="0" />
      </analyzer>
    </fieldType>

    <fieldType class="solr.TextField" name="text_synonym">
      <analyzer type="index">
        <tokenizer class="solr.WhitespaceTokenizerFactory"/>
        <filter class="solr.LowerCaseFilterFactory"/>
        <filter class="solr.SnowballPorterFilterFactory" language="English"/>
        <filter class="solr.FlattenGraphFilterFactory"/>
        <filter class="solr.RemoveDuplicatesTokenFilterFactory"/>
      </analyzer>
      <analyzer type="query">
        <tokenizer class="solr.WhitespaceTokenizerFactory"/>
        <filter class="solr.LowerCaseFilterFactory"/>
        <filter class="solr.SnowballPorterFilterFactory" language="English"/>
        <filter class="com.s24.search.solr.analysis.jdbc.JdbcSynonymFilterFactory" dataSource="jdbc/synonyms"
                sql="select stems_text from synonym where enabled = true" ignoreMissingDatabase="true"
                ignoreCase="true" expand="true"/>
        <filter class="solr.FlattenGraphFilterFactory"/>
        <filter class="solr.RemoveDuplicatesTokenFilterFactory"/>
      </analyzer>
    </fieldType>

    <fieldType class="solr.TextField" name="phrase_basic" positionIncrementGap="100">
      <analyzer type="index">
        <tokenizer class="solr.KeywordTokenizerFactory" />
        <filter class="solr.StandardFilterFactory" />
        <filter class="solr.LowerCaseFilterFactory" />
      </analyzer>
      <analyzer type="query">
        <tokenizer class="solr.KeywordTokenizerFactory" />
        <filter class="solr.StandardFilterFactory" />
        <filter class="solr.LowerCaseFilterFactory" />
      </analyzer>
    </fieldType>

    <fieldType class="solr.TextField" name="phrase_ngram">
      <analyzer type="index">
        <tokenizer class="solr.KeywordTokenizerFactory"/>
        <filter class="solr.LowerCaseFilterFactory"/>
        <filter class="solr.WordDelimiterGraphFilterFactory" catenateAll="1" splitOnNumerics="0" generateWordParts="0" generateNumberParts="0" />
        <filter class="solr.FlattenGraphFilterFactory" />
        <filter class="solr.NGramFilterFactory" minGramSize="3" maxGramSize="15" />
      </analyzer>
      <analyzer type="query">
        <tokenizer class="solr.KeywordTokenizerFactory"/>
        <filter class="solr.LowerCaseFilterFactory"/>
        <filter class="solr.WordDelimiterGraphFilterFactory" catenateAll="1" splitOnNumerics="0" generateWordParts="0" generateNumberParts="0" />
      </analyzer>
    </fieldType>
```
**text_basic**
Basic text field that tokenizes text into lowercase tokens without further analysis
Class: solr.TextField
Analyzer: Uses a lowercase tokenizer.

**text_stemmed**
Text field with minimal stemming, suitable for English text
Class: solr.TextField
Analyzer: Applies whitespace tokenization, standard filtering, lowercasing, word delimiter graph filtering, and minimal English stemming.

**text_stemmed_agro**
Provides more aggressive stemming for broader matching
Class: solr.TextField
Analyzer: Similar to text_stemmed but uses the Porter stemming algorithm for aggressive stemming.

**text_ngram**
Supports partial and wildcard matching through n-grams
Class: solr.TextField
Analyzer:
  - Index-Time: Applies n-gram filtering with minGramSize 1 and maxGramSize 15.
  - Query-Time: Does not apply n-gram filtering.

**text_synonym**
Handles synonyms during query time to improve search results
Class: solr.TextField
Analyzer:
  - Index-Time: Applies stemming and removes duplicates.
  - Query-Time: Adds synonym expansion from a JDBC data source.

**phrase_basic**
Suitable for exact phrase matching
Class: solr.TextField
Analyzer: Uses keyword tokenizer and lowercases the entire input as a single token.

**phrase_ngram**
Enhances phrase matching with n-gram analysis for partial matches
Class: solr.TextField
Analyzer:
  - Index-Time: Applies n-gram filtering with minGramSize 3 and maxGramSize 15.
  - Query-Time: Does not apply n-gram filtering.

**Numeric**
```
<fieldType name="pint" class="solr.IntPointField" docValues="true"/>
<fieldType name="pfloat" class="solr.FloatPointField" docValues="true"/>
<fieldType name="plong" class="solr.LongPointField" docValues="true"/>
<fieldType name="pdouble" class="solr.DoublePointField" docValues="true"/>
    
<fieldType name="pints" class="solr.IntPointField" docValues="true" multiValued="true"/>
<fieldType name="pfloats" class="solr.FloatPointField" docValues="true" multiValued="true"/>
<fieldType name="plongs" class="solr.LongPointField" docValues="true" multiValued="true"/>
<fieldType name="pdoubles" class="solr.DoublePointField" docValues="true" multiValued="true"/>
    
<fieldType name="int" class="solr.TrieIntField" docValues="true" precisionStep="0" positionIncrementGap="0"/>
<fieldType name="float" class="solr.TrieFloatField" docValues="true" precisionStep="0" positionIncrementGap="0"/>
<fieldType name="long" class="solr.TrieLongField" docValues="true" precisionStep="0" positionIncrementGap="0"/>
<fieldType name="double" class="solr.TrieDoubleField" docValues="true" precisionStep="0" positionIncrementGap="0"/>

<fieldType name="ints" class="solr.TrieIntField" docValues="true" precisionStep="0" positionIncrementGap="0" multiValued="true"/>
<fieldType name="floats" class="solr.TrieFloatField" docValues="true" precisionStep="0" positionIncrementGap="0" multiValued="true"/>
<fieldType name="longs" class="solr.TrieLongField" docValues="true" precisionStep="0" positionIncrementGap="0" multiValued="true"/>
<fieldType name="doubles" class="solr.TrieDoubleField" docValues="true" precisionStep="0" positionIncrementGap="0" multiValued="true"/>

<fieldType name="tint" class="solr.TrieIntField" docValues="true" precisionStep="8" positionIncrementGap="0"/>
<fieldType name="tfloat" class="solr.TrieFloatField" docValues="true" precisionStep="8" positionIncrementGap="0"/>
<fieldType name="tlong" class="solr.TrieLongField" docValues="true" precisionStep="8" positionIncrementGap="0"/>
<fieldType name="tdouble" class="solr.TrieDoubleField" docValues="true" precisionStep="8" positionIncrementGap="0"/>
    
<fieldType name="tints" class="solr.TrieIntField" docValues="true" precisionStep="8" positionIncrementGap="0" multiValued="true"/>
<fieldType name="tfloats" class="solr.TrieFloatField" docValues="true" precisionStep="8" positionIncrementGap="0" multiValued="true"/>
<fieldType name="tlongs" class="solr.TrieLongField" docValues="true" precisionStep="8" positionIncrementGap="0" multiValued="true"/>
<fieldType name="tdoubles" class="solr.TrieDoubleField" docValues="true" precisionStep="8" positionIncrementGap="0" multiValued="true"/>
```
Point-Based Numeric Fields (Efficient for numeric searches)
  - pint: Integer
  - pfloat: Float
  - plong: Long
  - pdouble: Double
  - pints, pfloats, plongs, pdoubles: Multi-valued versions

Trie-Based Numeric Fields (Traditional numeric fields)
  - int, float, long, double
  - ints, floats, longs, doubles: Multi-valued versions
    
Attributes:
	- docValues: Enabled for efficient sorting and faceting.
	- recisionStep: Controls indexing precision; 0 disables multi-precision indexing.

**Date**
```
<fieldType name="pdate" class="solr.DatePointField" docValues="true"/>
<fieldType name="pdates" class="solr.DatePointField" docValues="true" multiValued="true"/>
<fieldType name="date" class="solr.TrieDateField" docValues="true" precisionStep="0" positionIncrementGap="0"/>
<fieldType name="dates" class="solr.TrieDateField" docValues="true" precisionStep="0" positionIncrementGap="0" multiValued="true"/>
<fieldType name="tdate" class="solr.TrieDateField" docValues="true" precisionStep="6" positionIncrementGap="0"/>
<fieldType name="tdates" class="solr.TrieDateField" docValues="true" precisionStep="6" positionIncrementGap="0" multiValued="true"/>
```
Point-Based Date Fields
Efficient date fields for range queries
  - pdate
  - pdates: Multi-valued version

Trie-Based Date Fields
Traditional date fields with precision step for range queries
  - date
  - dates: Multi-valued version
    
#### Copy Fields
```
<copyField source="name" dest="name_suggest"/>
<copyField source="name" dest="name_select"/>
<copyField source="name" dest="name_single_term"/>
<copyField source="name" dest="name_stem_agro"/>
<copyField source="name" dest="name_synonym"/>
<copyField source="identifier" dest="identifier_select"/>
<copyField source="bn" dest="bn_select"/>
```
Copy fields are used to copy the contents of one field to another at index time. This is often used to index a field in multiple ways or to create composite fields. It enhance search capabilities by indexing data differently without altering the original data.
    
#### Analyzers and Filters
```
    <dynamicField name="*_ws" type="text_ws"  indexed="true"  stored="true"/>
    <fieldType name="text_ws" class="solr.TextField" positionIncrementGap="100">
      <analyzer>
        <tokenizer class="solr.WhitespaceTokenizerFactory"/>
      </analyzer>
    </fieldType>

    <fieldType name="text_general" class="solr.TextField" positionIncrementGap="100" multiValued="true">
      <analyzer>
        <tokenizer class="solr.StandardTokenizerFactory"/>
        <filter class="solr.StopFilterFactory" ignoreCase="true" words="stopwords.txt" />
        <filter class="solr.LowerCaseFilterFactory"/>
      </analyzer>
    </fieldType>
    <dynamicField name="*_txt_en" type="text_en"  indexed="true"  stored="true"/>
    <fieldType name="text_en" class="solr.TextField" positionIncrementGap="100">
      <analyzer>
        <tokenizer class="solr.StandardTokenizerFactory"/>
        <filter class="solr.StopFilterFactory"
                ignoreCase="true"
                words="lang/stopwords_en.txt"
            />
        <filter class="solr.LowerCaseFilterFactory"/>
        <filter class="solr.EnglishPossessiveFilterFactory"/>
        <filter class="solr.KeywordMarkerFilterFactory" protected="protwords.txt"/>
        <filter class="solr.PorterStemFilterFactory"/>
      </analyzer>
    </fieldType>
```
    
**Index-Time Analyzer**: Processes data when documents are added to the index.
**Query-Time Analyzer**: Processes search queries.
    
**solr.LowerCaseTokenizerFactory**: Converts text to lowercase and tokenizes it.
**solr.WhitespaceTokenizerFactory**: Splits text based on whitespace.
**solr.KeywordTokenizerFactory**: Treats the entire input as a single token.
    
#### Filters
Filters modify tokens produced by tokenizers.
 - solr.StandardFilterFactory
   Normalizes tokens (removes punctuation, etc).
 - solr.LowerCaseFilterFactory
   Converts tokens to lowercase.
 - solr.WordDelimiterGraphFilterFactory
   `<filter class="solr.WordDelimiterGraphFilterFactory" catenateAll="1" splitOnNumerics="0" generateWordParts="0" generateNumberParts="0" />`
   Splits words into subwords and performs various transformations.
   Attributes:
     - catenateAll="1": Concatenates all subwords.
	 - splitOnNumerics="0": Does not split tokens on numerics.
     - generateWordParts="0" and generateNumberParts="0": Prevents generation of word and number parts.
 - solr.FlattenGraphFilterFactory
   Simplifies the token graph, useful when dealing with synonyms or other filters that produce multiple tokens.
 - Stemming Filters
   - solr.EnglishMinimalStemFilterFactory: Applies minimal stemming for English.
   - solr.PorterStemFilterFactory: Applies Porter stemming algorithm for aggressive stemming.
   - solr.SnowballPorterFilterFactory: Uses Snowball stemming for the specified language.
 - solr.NGramFilterFactory
   - Generates n-grams (substrings) from tokens.
   Attributes:
     - minGramSize and maxGramSize: Define the size range of n-grams.
 - Synonym Filters
   ```
   <filter class="com.s24.search.solr.analysis.jdbc.JdbcSynonymFilterFactory" dataSource="jdbc/synonyms"
     sql="select stems_text from synonym where enabled = true" ignoreMissingDatabase="true"
     ignoreCase="true" expand="true"
   />
   ```
   com.s24.search.solr.analysis.jdbc.JdbcSynonymFilterFactory
   Fetches synonyms from a JDBC data source.
   Attributes:
     - dataSource: JDBC data source name.
	 - sql: SQL query to retrieve synonyms.
	 - ignoreMissingDatabase: Ignores errors if the database is missing.
	 - ignoreCase: Case-insensitive matching.
	 - expand: Whether to expand synonyms.
 - solr.RemoveDuplicatesTokenFilterFactory
   Removes duplicate tokens from the token stream.
    
## Trademark Core
```
  <queryResponseWriter name="json" class="solr.JSONResponseWriter">
    <str name="content-type">text/plain; charset=UTF-8</str>
  </queryResponseWriter>
```
Includes additional content-type settings - JSON responses are written as plain text

**`solr-data-config.xml`**
```
<dataConfig>
    <dataSource type="FileDataSource"/>
    <document>
        <entity name="processor" processor="FileListEntityProcessor" fileName=".*xml" recursive="true"
                rootEntity="false" dataSource="null" baseDir="/opt/solr/trademarks_data/latest">
            <entity name="trademark" processor="XPathEntityProcessor" forEach="/trademark"
                    url="${processor.fileAbsolutePath}">
                <field column="application_number" xpath="/trademark/application_number"/>
                <field column="category" xpath="/trademark/category"/>
                <field column="status" xpath="/trademark/status"/>
                <field column="name" xpath="/trademark/name"/>
                <field column="description" xpath="/trademark/description"/>
            </entity>
        </entity>
    </document>
</dataConfig>

```
Uses FileDataSource to read XML files.

Has a two-level entity structure:
  - processor entity: Uses FileListEntityProcessor to find XML files
  - trademark entity: Uses XPathEntityProcessor to extract trademark data

Reads from XML files in /opt/solr/trademarks_data/latest

Simpler field structure:
  - application_number
  - category
  - status
  - name
  - description
    
**`managed-schema`**
It includes extensive multi-language support.
    
```
<field name="application_number" type="string" multiValued="false" indexed="true" required="true" stored="true"/>
<field name="registration_number" type="string" multiValued="false" indexed="false" required="false" stored="true"/>
<field name="category" type="string" multiValued="false" indexed="false" required="false" stored="true"/>
<field name="description" type="text_general" multiValued="false" indexed="false" required="false" stored="true"/>
```

```
<field name="name_copy" type="text_name_copy" multiValued="false" indexed="true" stored="true"/>
<field name="name_with_synonyms" type="text_name_singular_synonyms" multiValued="false" indexed="true" stored="true"/>
<field name="name_compressed" type="text_name_compressed" multiValued="false" indexed="true" stored="true"/>
```

  - text_name_copy: Simple whitespace tokenization with lowercase
  - text_name_singular_synonyms: Complex analysis chain for trademark names with stemming and synonyms
  - text_name_compressed: Special field type that removes company designations and normalizes text
    
<u>Complex name compression processing</u>
```
<fieldType name="text_name_compressed" class="solr.TextField">
    <analyzer>
        <!-- Extensive list of company designation removals -->
        <filter class="solr.PatternReplaceFilterFactory" pattern=" CORP." replacement="" replace="all"/>
        <filter class="solr.PatternReplaceFilterFactory" pattern=" CORPORATION" replacement="" replace="all"/>
        <!-- Multiple other company designation patterns -->
        ...
    </analyzer>
</fieldType>
```
    
<u>Name Field Configuration</u>
`<field name="name" type="text_en_splitting" multiValued="false" indexed="true" required="false" stored="true" termVectors="true"/>`

termVectors="true" for more advanced text analysis

<u>Unique Copy Field Directives</u>
```
<copyField source="name" dest="name_copy"/>
<copyField source="name" dest="name_with_synonyms"/>
<copyField source="name" dest="name_compressed"/>
```

## possible.conflicts Core

**Query Parser Configuration**
```
<!-- Query Parsers
     https://cwiki.apache.org/confluence/display/solr/Query+Syntax+and+Parsing
     Multiple QParserPlugins can be registered by name, and then
     used in either the "defType" param for the QueryComponent (used
     by SearchHandler) or in LocalParams
-->

<!--
   <queryParser name="myparser" class="com.mycompany.MyQParserPlugin"/>
-->
```
Provides framework for custom query parsing implementations
Allows registration of multiple parser plugins
Can be used with defType parameter or LocalParams
Enables customization of query syntax interpretation

**Function Parser Configuration**
```
<!-- Function Parsers
     http://wiki.apache.org/solr/FunctionQuery
     Multiple ValueSourceParsers can be registered by name, and then
     used as function names when using the "func" QParser.
-->

<!--
   <valueSourceParser name="myfunc" class="com.mycompany.MyValueSourceParser" />
-->
```
Enables custom function query implementations
Allows registration of multiple ValueSourceParsers
Can be used with the "func" QParser
Supports custom scoring and ranking functions

**Document Transformers Configuration**
```
<!-- Document Transformers
     http://wiki.apache.org/solr/DocTransformers
-->

<!--
   <transformer name="db" class="com.mycompany.LoadFromDatabaseTransformer" >
     <int name="connection">jdbc://....</int>
   </transformer>
-->

<!--
   <transformer name="mytrans2" class="org.apache.solr.response.transform.ValueAugmenterFactory" >
     <int name="value">5</int>
   </transformer>
-->

<!--
   <transformer name="mytrans3" class="org.apache.solr.response.transform.ValueAugmenterFactory" >
     <double name="defaultValue">5</double>
   </transformer>
-->

<!--
   <transformer name="qecBooster" class="org.apache.solr.response.transform.EditorialMarkerFactory" />
-->
```
Enables document transformation during query response
Supports integration with external data sources
Allows dynamic value augmentation
Provides boosting and editorial marking capabilities

**Select RequestHandler Configuration**
```
<requestHandler name="/select" class="solr.SearchHandler">
    <lst name="defaults">
      <str name="echoParams">explicit</str>
      <int name="rows">10</int>
      ...
    </lst>
</requestHandler>
```
    
**`solr-data-config.xml`**
```
<dataSource 
    name="corp-conflicts-ds"
    type="com.s24.search.solr.analysis.jdbc.DataImportJdbcDataSource"
    dataSource="jdbc/bcrs_corps" />

<dataSource 
    name="name-conflicts-ds"
    type="com.s24.search.solr.analysis.jdbc.DataImportJdbcDataSource"
    dataSource="jdbc/bcrs_names" />
```
`bc_registries` for corporate conflicts
`bc_registries_names` for name conflicts
Clear separation of concerns
  - Name: corp-conflicts-ds (identifies the corporate conflicts data source)
    Type: Uses com.s24.search.solr.analysis.jdbc.DataImportJdbcDataSource
    DataSource: Points to jdbc/bcrs_corps JNDI resource
    Purpose: Handles corporate registry conflicts
  - Name: name-conflicts-ds (identifies the name conflicts data source)
    Type: Uses same DataImport JDBC data source type
    DataSource: Points to jdbc/bcrs_names JNDI resource
    Purpose: Handles business name conflicts

```
<entity 
    name="corp-conflicts" 
    dataSource="corp-conflicts-ds" 
    pk="id"
    query="SELECT * FROM bc_registries.solr_dataimport_conflicts_vw" />

<entity 
    name="name-conflicts" 
    dataSource="name-conflicts-ds" 
    pk="id"
    query="SELECT * FROM bc_registries_names.solr_dataimport_conflicts_vw" />
```
Uses solr_dataimport_conflicts_vw views
Encapsulates conflict detection logic
Consistent naming across schemas
  - Name: corp-conflicts
    DataSource: References corp-conflicts-ds
    Primary Key: Uses id field
    Query: Selects from bc_registries.solr_dataimport_conflicts_vw view
    Schema: Uses bc_registries schema
  - Name: name-conflicts
    DataSource: References name-conflicts-ds
    Primary Key: Uses id field
    Query: Selects from bc_registries_names.solr_dataimport_conflicts_vw view
    Schema: Uses bc_registries_names schema
    
**`managed-schmea`**
    
<u>Unique Required Fields</u>
```
<field name="id" type="string" stored="true" required="true" indexed="true" multiValued="false"/>
<field name="name" type="text_en_splitting" multiValued="false" indexed="true" required="true" stored="true" termVectors="true"/>
<field name="source" type="string" multiValued="false" indexed="true" required="true" stored="true"/>
```
    
<u>Special Purpose Fields</u>
```
<field name="state_type_cd" type="string" multiValued="false" indexed="true" required="false" stored="true" termVectors="true"/>
<field name="start_date" type="pdate" docValues="true" multiValued="false" indexed="false" required="false" stored="true"/>
<field name="jurisdiction" type="string" multiValued="false" indexed="false" required="false" stored="true"/>
```
    
<u>Name Analysis Fields</u>
```
<field name="name_copy" type="text_name_copy" multiValued="false" indexed="true" stored="true"/>
<field name="name_with_synonyms" type="text_name_singular_synonyms" multiValued="false" indexed="true" stored="true"/>
<field name="name_compressed" type="text_name_compressed" multiValued="false" indexed="true" stored="true"/>
<field name="name_exact_match" type="text_name_exact_match" multiValued="false" indexed="true" stored="true"/>
```

 - `text_name_copy`
   Uses WhitespaceTokenizer
   Simple lowercase processing
   No synonym expansion

 - `text_name_singular_synonyms`
   Includes snowball stemming
   Synonym handling at query time
   Duplicate removal

 - `text_name_compressed`
   Removes business designations
   Strips whitespace and non-alpha characters
   KeywordTokenizer for whole phrase matching

 - `name_no_synonyms`
   Complex character filtering
   British Columbia abbreviation handling
   No synonym expansion

<u>Phonetic Analysis Fields</u>
```
<field name="dblmetaphone_name" type="dblmetaphone_name" multiValued="false" indexed="true" stored="true"/>
<field name="cobrs_phonetic" type="cobrs_phonetic" multiValued="false" indexed="true" stored="true"/>
```

 - `cobrs_phonetic`
   Custom phonetic algorithm
   Number word conversion
   Special character handling
   British Columbia abbreviation normalization

 - `dblmetaphone_name`
   Double Metaphone algorithm
   Special character handling
   British Columbia abbreviation normalization

<u>Special Processing Fields</u>
```
<field name="txt_starts_with" type="txt_starts_with" multiValued="false" indexed="true" stored="false"/>
<field name="name_no_synonyms" type="name_no_synonyms" multiValued="false" indexed="true" stored="false"/>
<field name="contains_exact_phrase" type="contains_exact_phrase" multiValued="false" indexed="true" stored="true"/>
```
 - `text_name_exact_match`
   Removes business designations
   Removes special characters
   Compressed format for exact matching


 - `txt_starts_with`
   Complex stopword removal
   Special character handling
   British Columbia abbreviation normalization


 - `contains_exact_phrase`
   Minimal processing
   Preserves word boundaries
   Lowercase conversion
    
<u>Currency Symbol Handling</u>
```
<charFilter class="solr.PatternReplaceCharFilterFactory" pattern="(^|\s+)(\$+(\s+|$))+" replacement="$1dollar$3" />
<charFilter class="solr.PatternReplaceCharFilterFactory" pattern="\$" replacement="s" />
```
    
<u>British Columbia Abbreviations</u>
```
<charFilter class="solr.PatternReplaceCharFilterFactory" 
    pattern="([B|b][R|r][I|i][T|t][I|i][S|s][H|h][\W][C|c][O|o][L|l][U|u][M|m][B|b][I|i][A|a][N|n][\W|$|s|S])"
    replacement="bc" />
```
    
<u>Token filter</u>
```
Complex Work Handling
    
<filter class="solr.WordDelimiterGraphFilterFactory" 
    catenateNumbers="1" generateNumberParts="0" splitOnCaseChange="0" 
    generateWordParts="0" catenateAll="1" catenateWords="1"/>
```
    
```
Special Processing
    
<filter class="solr.LimitTokenCountFilterFactory" maxTokenCount="60" consumeAllTokens="false" />
<filter class="solr.RemoveDuplicatesTokenFilterFactory"/>
```
    
## Names Core

**`solr-data-config.xml`**
```
<dataConfig>
    <dataSource type="com.s24.search.solr.analysis.jdbc.DataImportJdbcDataSource" dataSource="jdbc/bcrs_names" />
    <document>
        <entity name="name_instance" pk="id" query="SELECT * FROM bc_registries_names.solr_dataimport_names_vw" />
    </document>
</dataConfig>
```

Uses a custom JDBC data source implementation com.s24.search.solr.analysis.jdbc.DataImportJdbcDataSource
References a JDBC data source named "jdbc/bcrs_names"
This appears to be connecting to a BC Registries names database
```
<dataSource type="com.s24.search.solr.analysis.jdbc.DataImportJdbcDataSource" 
           dataSource="jdbc/bcrs_names" />
```
    
Defines a single entity named "name_instance"
Uses "id" as the primary key field
Imports data from a view named solr_dataimport_names_vw in the bc_registries_names schema
The view likely contains pre-formatted data ready for Solr indexing
```
<document>
    <entity name="name_instance" 
            pk="id" 
            query="SELECT * FROM bc_registries_names.solr_dataimport_names_vw" />
</document>
```

**`managed-schema`**
<u>Core Business Name Fields</u>
```
<!-- Primary Identifier & Name Fields -->
<field name="id" type="string" stored="true" required="true" indexed="true" multiValued="false"/>
<field name="name" type="text_en_splitting" multiValued="false" indexed="true" required="true" stored="true" termVectors="true"/>

<!-- Administrative Fields -->
<field name="nr_num" type="string" multiValued="false" indexed="false" required="false" stored="true"/>
<field name="submit_count" type="plong" docValues="true" multiValued="false" indexed="false" required="false" stored="true"/>
<field name="name_state_type_cd" type="string" multiValued="false" indexed="false" required="false" stored="true"/>
<field name="start_date" type="pdate" docValues="true" multiValued="false" indexed="false" required="false" stored="true"/>
<field name="jurisdiction" type="string" multiValued="false" indexed="false" required="false" stored="true"/>
```
    
<u>Specialized Name Analysis Fields</u>
```
<!-- Multiple Analysis Fields for Different Search Types -->
<field name="name_copy" type="text_name_copy" multiValued="false" indexed="true" stored="true"/>
<field name="name_with_synonyms" type="text_name_singular_synonyms" multiValued="false" indexed="true" stored="true"/>
<field name="name_compressed" type="text_name_compressed" multiValued="false" indexed="true" stored="true"/>
<field name="name_exact_match" type="text_name_exact_match" multiValued="false" indexed="true" stored="true"/>
```
    
<u>Name-Specific Field Types</u>
```
<fieldType name="text_name_copy" class="solr.TextField" positionIncrementGap="100" multiValued="true">
  <analyzer type="index">
    <tokenizer class="solr.WhitespaceTokenizerFactory"/>
    <filter class="solr.LowerCaseFilterFactory"/>
  </analyzer>
  <analyzer type="query">
    <tokenizer class="solr.WhitespaceTokenizerFactory"/>
    <filter class="solr.LowerCaseFilterFactory"/>
  </analyzer>
</fieldType>
```
    
```
<fieldType name="text_name_singular_synonyms" class="solr.TextField" positionIncrementGap="100" multiValued="true">
  <analyzer type="index">
    <tokenizer class="solr.WhitespaceTokenizerFactory"/>
    <filter class="solr.StopFilterFactory" words="lang/stopwords_en.txt" ignoreCase="true"/>
    <filter class="solr.LowerCaseFilterFactory"/>
    <filter class="solr.PorterStemFilterFactory"/>
    <filter class="solr.WordDelimiterGraphFilterFactory" catenateNumbers="1" generateNumberParts="0" splitOnCaseChange="0" generateWordParts="0" catenateAll="1" catenateWords="1"/>
    <filter class="solr.FlattenGraphFilterFactory"/>
    <filter class="solr.RemoveDuplicatesTokenFilterFactory"/>
  </analyzer>
</fieldType>
```
    
```
<fieldType name="text_name_compressed" class="solr.TextField" positionIncrementGap="100" multiValued="true">
  <analyzer>
    <!-- Business Designation Removal -->
    <filter class="solr.PatternReplaceFilterFactory" pattern=" CORP." replacement="" replace="all"/>
    <filter class="solr.PatternReplaceFilterFactory" pattern=" CORPORATION" replacement="" replace="all"/>
    <filter class="solr.PatternReplaceFilterFactory" pattern=" INC." replacement="" replace="all"/>
    <!-- Multiple other business designations -->
    
    <!-- Character Normalization -->
    <filter class="solr.PatternReplaceFilterFactory" pattern="'s " replacement="" />
    <filter class="solr.PatternReplaceFilterFactory" pattern="[^\w]+" replacement="" replace="all"/>
    <tokenizer class="solr.KeywordTokenizerFactory"/>
    <filter class="solr.LowerCaseFilterFactory"/>
  </analyzer>
</fieldType>
```
    
```
<fieldType name="text_name_exact_match" class="solr.TextField" positionIncrementGap="100" multiValued="false">
  <analyzer type="index">
    <tokenizer class="solr.KeywordTokenizerFactory"/>
    <filter class="solr.LowerCaseFilterFactory"/>
    <!-- Extensive business designation removal -->
    <!-- Character and whitespace normalization -->
    <!-- Duplicate character removal -->
  </analyzer>
</fieldType>    
```
    
<u>Copy field</u>
```
<copyField source="name" dest="name_copy"/>
<copyField source="name" dest="name_with_synonyms"/>
<copyField source="name" dest="name_compressed"/>
<copyField source="name" dest="name_exact_match"/>
```